import { useState, useEffect } from 'react';
import { queryData, countTokens } from '../services/api';
import './QueryAnalysis.css';

// Gemini 2.5 Flash Pricing
const GEMINI_PRICING = {
    INPUT_PER_MILLION: 0.15,
    OUTPUT_PER_MILLION: 0.60,
};

const calculateCost = (inputTokens, outputTokens) => {
    const cost =
        (inputTokens / 1_000_000) * GEMINI_PRICING.INPUT_PER_MILLION +
        (outputTokens / 1_000_000) * GEMINI_PRICING.OUTPUT_PER_MILLION;
    return cost.toFixed(6);
};

// Debounce helper
const useDebounce = (value, delay) => {
    const [debouncedValue, setDebouncedValue] = useState(value);
    useEffect(() => {
        const handler = setTimeout(() => setDebouncedValue(value), delay);
        return () => clearTimeout(handler);
    }, [value, delay]);
    return debouncedValue;
};

function QueryAnalysis() {
    const [dataFormat, setDataFormat] = useState('JSON');
    const [dataInput, setDataInput] = useState('[{"id": 1, "name": "Alice", "age": 30}, {"id": 2, "name": "Bob", "age": 25}]');
    const [question, setQuestion] = useState('');
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [inputTokenCount, setInputTokenCount] = useState(0);
    const [isCounting, setIsCounting] = useState(false);

    const debouncedDataInput = useDebounce(dataInput, 1000);

    useEffect(() => {
        const fetchTokenCount = async () => {
            if (!debouncedDataInput.trim()) {
                setInputTokenCount(0);
                return;
            }
            setIsCounting(true);
            try {
                const data = await countTokens(debouncedDataInput);
                setInputTokenCount(data.count);
            } catch (err) {
                console.error("Failed to count tokens:", err);
            } finally {
                setIsCounting(false);
            }
        };

        fetchTokenCount();
    }, [debouncedDataInput]);

    const exampleQuestions = [
        "What's the average age?",
        "List all names",
        "How many items?",
        "Summarize data"
    ];

    const handleExampleClick = (q) => {
        setQuestion(q);
    };

    const handleAnalyze = async () => {
        if (!question.trim()) {
            setError('Please enter a question');
            return;
        }
        if (!dataInput.trim()) {
            setError('Please provide data to analyze');
            return;
        }

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const data = await queryData(dataInput, question, dataFormat);

            // Clean up the answer - remove markdown code fences and "Answer" labels
            let cleanAnswer = data.answer.trim();

            // Remove "Answer" or similar labels at the start
            cleanAnswer = cleanAnswer.replace(/^(Answer|Response|Result|Output)[\s:]*\n*/i, '');

            // Remove markdown code fences (```json, ```toon, etc.)
            cleanAnswer = cleanAnswer.replace(/```[a-z]*\n?/g, '');
            cleanAnswer = cleanAnswer.replace(/```\n?/g, '');

            // Trim again after cleanup
            cleanAnswer = cleanAnswer.trim();

            data.answer = cleanAnswer;
            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="query-container">
            <div className="query-main">
                <div className="data-section">
                    <h2>1. Select Format & Enter Data</h2>

                    <div className="format-selector-top">
                        <label className={`format-option ${dataFormat === 'JSON' ? 'active' : ''}`}>
                            <input
                                type="radio"
                                value="JSON"
                                checked={dataFormat === 'JSON'}
                                onChange={(e) => setDataFormat(e.target.value)}
                            />
                            <span>JSON</span>
                        </label>
                        <label className={`format-option ${dataFormat === 'TOON' ? 'active' : ''}`}>
                            <input
                                type="radio"
                                value="TOON"
                                checked={dataFormat === 'TOON'}
                                onChange={(e) => setDataFormat(e.target.value)}
                            />
                            <span>TOON</span>
                        </label>
                    </div>

                    <div className="input-wrapper">
                        <textarea
                            className="code-input"
                            value={dataInput}
                            onChange={(e) => setDataInput(e.target.value)}
                            placeholder={`Paste your ${dataFormat} data here...`}
                            disabled={!dataFormat}
                        />
                        <div className="realtime-token-count">
                            {isCounting ? 'Counting...' : `${dataFormat} Tokens: ${inputTokenCount}`}
                        </div>
                    </div>
                </div>

                <div className="question-section">
                    <h2>2. Ask a Question</h2>
                    <input
                        type="text"
                        className="question-input"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        placeholder="e.g., What's the average age?"
                        disabled={!dataInput.trim()}
                        onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
                    />

                    <div className="examples">
                        <span className="examples-label">Examples:</span>
                        <div className="example-buttons">
                            {exampleQuestions.map((eq, i) => (
                                <button
                                    key={i}
                                    className="btn-example"
                                    onClick={() => handleExampleClick(eq)}
                                    disabled={!dataInput.trim()}
                                >
                                    {eq}
                                </button>
                            ))}
                        </div>
                    </div>

                    <button
                        className="btn-analyze"
                        onClick={handleAnalyze}
                        disabled={loading || !dataInput.trim() || !question.trim()}
                    >
                        {loading ? '🔍 Analyzing...' : '🔍 Analyze'}
                    </button>

                    {error && (
                        <div className="error-message">
                            <strong>Error:</strong> {error}
                        </div>
                    )}
                </div>
            </div>

            {result && (
                <div className="results-section">
                    <div className="answer-box">
                        <h2>Answer</h2>
                        <div className="answer-content">{result.answer}</div>
                    </div>

                    <div className="token-analysis-container">
                        <div className="analysis-section">
                            <h3>Token Usage Breakdown</h3>

                            {/* Input Section */}
                            <div className="token-section">
                                <h4>📥 Input Tokens</h4>
                                <div className="breakdown-grid">
                                    <div className="breakdown-item">
                                        <span className="label">Data ({result.data_format})</span>
                                        <span className="value">{result.breakdown.data_tokens}</span>
                                    </div>
                                    <div className="breakdown-item">
                                        <span className="label">Question</span>
                                        <span className="value">{result.breakdown.question_tokens}</span>
                                    </div>
                                    <div className="breakdown-item">
                                        <span className="label">System Prompt</span>
                                        <span className="value">{result.breakdown.template_tokens}</span>
                                    </div>
                                    <div className="breakdown-item total">
                                        <span className="label">Total Input</span>
                                        <span className="value">{result.prompt_tokens}</span>
                                    </div>
                                </div>
                            </div>

                            {/* Output Section */}
                            <div className="token-section">
                                <h4>📤 Output Tokens</h4>
                                <div className="breakdown-grid">
                                    <div className="breakdown-item">
                                        <span className="label">AI Response ({result.data_format})</span>
                                        <span className="value">{result.completion_tokens}</span>
                                    </div>
                                </div>
                            </div>

                            {/* Total Section */}
                            <div className="token-section">
                                <h4>💰 Total Cost</h4>
                                <div className="breakdown-grid">
                                    <div className="breakdown-item total">
                                        <span className="label">Total Tokens</span>
                                        <span className="value">{result.total_llm_tokens}</span>
                                    </div>
                                    <div className="breakdown-item cost">
                                        <span className="label">Cost</span>
                                        <span className="value">
                                            ${calculateCost(result.prompt_tokens, result.completion_tokens)}
                                        </span>
                                    </div>
                                </div>
                                <div className="pricing-info">
                                    Pricing: ${GEMINI_PRICING.INPUT_PER_MILLION} per million tokens in • ${GEMINI_PRICING.OUTPUT_PER_MILLION} per million tokens out
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default QueryAnalysis;

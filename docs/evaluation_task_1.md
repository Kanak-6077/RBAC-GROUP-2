\# Task 1: Evaluation of Model Predictions



\## 1. Introduction



Traditional accuracy metrics such as classification accuracy are not suitable for

Large Language Models (LLMs), especially when used in Retrieval-Augmented Generation (RAG)

systems. This task focuses on evaluating the performance of an RBAC-based RAG system

by analyzing document retrieval quality, answer generation quality, access control

correctness, and system stability.



---



\## 2. Evaluation Methodology



The evaluation was performed using the following methods:



\### 2.1 Retrieval Evaluation

To measure the effectiveness of document retrieval from the vector database,

Precision@K and Recall@K metrics were used.



\- \*\*Precision@K\*\* measures the proportion of relevant documents among the top K retrieved documents.

\- \*\*Recall@K\*\* measures whether the relevant document was successfully retrieved.



\### 2.2 Answer Quality Evaluation

Since the system generates free-form text responses, traditional accuracy metrics

are not applicable. Human evaluation was used instead, based on:

\- Relevance

\- Correctness

\- Completeness



Each response was scored on a scale of 1 to 4.



\### 2.3 RBAC Evaluation

RBAC evaluation was conducted to verify whether users could only access documents

permitted by their assigned roles.



\### 2.4 Confidence and Stability Analysis

Confidence scores returned by the system were analyzed to check consistency

across different queries.



---



\## 3. Experimental Setup



\- \*\*Architecture\*\*: Retrieval-Augmented Generation (RAG)

\- \*\*LLM\*\*: Ollama (local inference)

\- \*\*Dataset\*\*:

&nbsp; - Marketing reports (Q1–Q4, 2024)

&nbsp; - HR structured CSV and policy documents

\- \*\*User Role for Evaluation\*\*: Admin

\- \*\*Number of Queries Tested\*\*: 10



All evaluation queries were executed using the Admin role to assess the full

capability of the system. RBAC validation was performed separately.



---



\## 4. Retrieval Evaluation Results



| Query | Expected Document | Retrieved Documents | Precision@K | Recall@K |

|------|------------------|-------------------|-------------|----------|

| Q1 marketing summary | marketing\_report\_2024.md | Q3, Q2, Q4, 2024 | 0.25 | 1.0 |

| Q2 marketing summary | marketing\_report\_q2\_2024.md | Q3, 2024, Q2, Q4 | 0.25 | 1.0 |

| Q3 marketing summary | marketing\_report\_q3\_2024.md | Q3, 2024, Q2, Q4 | 0.25 | 1.0 |

| Q4 marketing summary | market\_report\_q4\_2024.md | Q3, Q2, Q4, 2024 | 0.25 | 1.0 |

| Marketing trends | marketing\_report\_2024.md | 2024, Q2, Q4 | 0.33 | 1.0 |

| HR insights | hr\_data.csv | hr\_data, handbook, engineering | 0.33 | 1.0 |

| HR departments | hr\_data.csv | hr\_data, handbook | 0.50 | 1.0 |

| Employee distribution | hr\_data.csv | hr\_data, handbook | 0.50 | 1.0 |

| HR issues | employee\_handbook.md | hr\_data, handbook, engineering | 0.33 | 1.0 |

| Salary trends | hr\_data.csv | hr\_data, handbook | 0.50 | 1.0 |



\*\*Observation:\*\*  

The system achieved 100% recall across all queries, indicating that relevant documents

were consistently retrieved. Moderate precision values are expected in RAG systems

due to contextual overlap among documents.



---



\## 5. Answer Quality Evaluation Results



| Query | Relevance | Correctness | Completeness |

|------|-----------|------------|--------------|

| Q1 marketing summary | 4 | 4 | 4 |

| Q2 marketing summary | 4 | 4 | 4 |

| Q3 marketing summary | 4 | 3 | 3 |

| Q4 marketing summary | 4 | 4 | 4 |

| Marketing trends | 3 | 3 | 2 |

| HR insights | 2 | 3 | 2 |

| HR departments | 4 | 4 | 4 |

| Employee distribution | 4 | 4 | 3 |

| HR issues | 3 | 3 | 3 |

| Salary trends | 2 | 3 | 2 |



\*\*Observation:\*\*  

Marketing-related queries produced highly relevant and correct answers. HR analytical

queries showed slightly lower completeness due to limited numerical aggregation

in the source documents.



---



\## 6. RBAC Evaluation Results



| Role | Query | Expected Access | Result |

|------|------|----------------|--------|

| Marketing | HR salary trends | Denied | Correct |

| HR | Marketing Q2 performance | Denied | Correct |

| Admin | All queries | Allowed | Correct |



\*\*RBAC Accuracy:\*\* 100%



---



\## 7. Confidence Score Analysis



| Query Type | Confidence Score |

|------------|----------------|

| Marketing queries | 0.9 |

| HR queries | 0.9 |



The confidence score remained consistent across different queries,

indicating stable system behavior.



---



\## 8. Conclusion



The RBAC-based RAG system demonstrates effective document retrieval, high-quality

answer generation, and reliable access control enforcement. The evaluation confirms

that the system performs well for enterprise-style document-based question answering,

with scope for future improvements in precision optimization and structured data handling. 


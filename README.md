# EightFoldAI Finals - Intelligent Resume & Recommendation Analysis System

**Team Trial | September 2024**

An AI-powered system that transforms unstructured resume and recommendation letter data into structured, actionable insights for HR and recruitment teams. The platform leverages advanced NLP techniques to detect fraud, assess candidate credibility, and provide intelligent hiring recommendations.

---

## 🎯 Overview

This system addresses critical challenges in the hiring process by:
- Converting unstructured PDF resumes and recommendation letters into structured data
- Detecting fraudulent claims and inconsistencies across documents
- Evaluating candidate influence and industry credibility
- Providing risk and hiring scores for informed decision-making
- Enabling advanced semantic and keyword-based candidate search

![System Overview](Figure 1: Overview)

---

## 🚀 Key Features

### 1. **Resume Structuring**
Automatically extracts and structures:
- **Work Experience**: Role names, descriptions, company size/level, employment dates
- **Education**: University, dates, degree/domain, education level
- **Skills & Interests**: Projects, interests, and skill proficiency levels (0-5 scale)

#### Skill Level Benchmarks
- **Level 5**: Expert - Led major projects, go-to resource
- **Level 4**: Strong proficiency with extensive experience, mentors others
- **Level 3**: Solid working proficiency, minimal supervision needed
- **Level 2**: Some practical experience in limited situations
- **Level 1**: Basic familiarity with minimal exposure
- **Level 0**: Mentioned but not backed by experience

### 2. **Recommendation Letter Analysis**
Cross-references recommendation letters with structured resumes to determine:

**Relevance Score (1-10)**
- 1-3: Low alignment with resume
- 4-6: Moderate connection to key areas
- 7-9: High alignment with strong details
- 10: Exceptional, full alignment with all qualifications

**Fraud Detection (1-5)**
- 1: Genuine, well-supported
- 2: Minor inconsistencies
- 3: Multiple exaggerated claims
- 4: Unrealistic aspects, improbable claims
- 5: Obvious signs of fraud

**Verified Skills**
- Cross-validates skills mentioned across resume, work history, and recommendations
- Assigns confidence scores based on supporting evidence

### 3. **Industry Influence Scoring**
Calculates influence factor (0-10) based on:

- **Job Role Level (1-5 points)**
  - Executive Leadership (CEO, CFO, CTO): 5 points
  - Senior Management (Director, Senior Manager): 4 points
  - Middle Management (Manager, Team Lead): 3 points
  - Professional Staff (Senior Engineer, Specialist): 2 points
  - Entry-Level (Junior positions): 1 point

- **Company Size & Influence (1-3 points)**
  - Fortune 500, Global Brands: 3 points
  - Medium-sized, Regional Leaders: 2 points
  - Startups, Small Businesses: 1 point

- **Experience & Tenure (0-2 points)**
  - 10+ years: 2 points
  - 3-10 years: 1 point
  - <3 years: 0 points

### 4. **Risk Score Calculation**
Comprehensive fraud risk assessment incorporating:
- Fraud scores from recommendation letters
- Cycle detection in peer recommendations (DFS algorithm)
- Recommender credibility analysis

**Formula**: 
```
Base Fraud Score = Σ(xi - 1) / 4n
```
Where xi = individual fraud scores

**Penalties**:
- Cycles of 3 people: -10% safety score
- Cycles of 4: -8%
- Cycles of 5: -6%
- Cycles of 6: -4%
- Recommender with fraud score 4: -10% safety
- Recommender with fraud score 5: -20% safety

### 5. **Hiring Score**
Weighted recommendation system considering:
```
Hiring Score = x · [influence(i)]^1.5 · (1 - risk/100)^2
```
Where:
- x = weighted mean of relevance scores
- Weights proportional to (recommender's safety score)²

### 6. **Advanced Search**
Hybrid search combining:
- **Semantic Search**: paraphrase-MiniLM-L12-v2 embeddings with cosine similarity
- **Keyword Search**: BM25 algorithm
- Job history text analysis for better candidate matching

---

## 🛠️ Technology Stack

### AI/ML
- **LLM**: Llama-70B (hosted on Groq Cloud)
- **Embeddings**: paraphrase-MiniLM-L12-v2
- **Algorithms**: DFS (cycle detection), BM25 (keyword search), Cosine Similarity

### Backend
- **Framework**: Flask
- **Processing**: Python

### Frontend
- **Framework**: React
- **Styling**: Tailwind CSS

---

## 📊 Candidate Comparison
![Candidate Comparison Interface](Figure 2: Candidate Comparison)

---

## ⚖️ Bias & Fairness Considerations

The system acknowledges and addresses potential biases:

1. **NGO Impact**: Recognized NGOs receive 2/3 company influence, but may have larger social impact through social media not captured in scoring
2. **Company Size vs. Role**: A CEO at a small company may receive lower influence than an associate at a Fortune 500 company
3. **Configurable Weights**: Company size (weight: 3) and positional hierarchy (weight: 5) can be adjusted as more data flows in

---

## 🔧 Scalability & Optimization

### Performance Enhancements
- **ONNX Runtime**: Accelerate embedding creation
- **Vector Databases**: Milvus or Pinecone with HNSW algorithm (O(log n) complexity)
- **Model Optimization**: LoRA for reducing LLM size while maintaining performance

### Infrastructure
- **Backend**: AWS Lambda for auto-scaling
- **Frontend**: AWS or Netlify deployment
- **Cost**: Llama 3-70B costs ~$0.90 per million tokens

---

## 💰 Cost Analysis

- **LLM Processing**: $0.90 per million tokens (Llama 3-70B via Groq)
- **Hosting**: Scalable cloud infrastructure (AWS Lambda)
- **Optimization**: LoRA fine-tuning reduces costs further

---

## 📈 Performance Metrics

The system provides comprehensive analytics including:
- Risk scores for fraud detection
- Hiring scores for candidate ranking
- Influence factors for credibility assessment
- Verified skill mappings
- Advanced search relevance scoring

---

## 🎯 Use Cases

- **HR Teams**: Automate resume screening and verification
- **Recruitment Agencies**: Detect fraudulent applications at scale
- **Enterprise Hiring**: Evaluate candidate credibility and fit
- **Background Verification**: Cross-reference claims across documents

---

## 🔐 Fraud Detection Capabilities

- Informal language detection in recommendations
- Statistically improbable claims analysis
- Cross-document consistency checking
- Peer recommendation cycle detection
- Recommender credibility tracking

---

## 📝 Future Enhancements

- Real-time processing pipeline
- Multi-language support
- Integration with ATS systems
- Machine learning model retraining pipeline
- Enhanced bias detection and mitigation

---

## 👥 Team

Team Trial - September 2024

---


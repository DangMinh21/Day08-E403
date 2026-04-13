# Day08-E403: RAG Agent Deployment

## Overview
This repository contains the materials and code for Day 08 of the Practical AI course. The focus of this session is on deploying Retrieval-Augmented Generation (RAG) agents. The repository includes lecture notes, lab exercises, and supporting resources.

## Repository Structure

```
lecture-08.html          # Lecture slides for Day 08
PLAN.md                  # Plan and objectives for the day
lab/                     # Lab exercises and related files
  eval.py                # Evaluation script for the RAG agent
  index.py               # Script for indexing documents
  rag_answer.py          # Main script for answering queries using RAG
  README.md              # Lab-specific README
  requirements.txt       # Python dependencies for the lab
  SCORING.md             # Scoring guidelines for the lab
  chroma_db/             # Directory for Chroma database
    chroma.sqlite3       # SQLite database file for Chroma
  data/                  # Data files for the lab
    test_questions.json  # Test questions for evaluation
    docs/                # Documents for indexing
      access_control_sop.txt
      hr_leave_policy.txt
      it_helpdesk_faq.txt
      policy_refund_v4.txt
      sla_p1_2026.txt
  docs/                  # Additional documentation
    architecture.md      # Architecture notes
    tuning-log.md        # Tuning logs for the RAG agent
  reports/               # Reports directory
    individual/          # Individual reports
      template.md        # Report template
```

## Key Files

- **lecture-08.html**: Contains the lecture slides for Day 08.
- **lab/**: Contains all the lab-related files, including scripts, data, and documentation.
  - **eval.py**: Script for evaluating the RAG agent.
  - **index.py**: Script for creating the document index.
  - **rag_answer.py**: Main script for answering queries using the RAG agent.
  - **requirements.txt**: Lists the Python dependencies required for the lab.
  - **SCORING.md**: Guidelines for scoring the lab exercises.
  - **chroma_db/**: Directory containing the Chroma database file.
  - **data/**: Contains test questions and documents for indexing.
  - **docs/**: Additional documentation, including architecture notes and tuning logs.
  - **reports/**: Directory for individual reports.

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r lab/requirements.txt
   ```

2. **Run the Indexing Script**:
   ```bash
   python lab/index.py
   ```

3. **Evaluate the RAG Agent**:
   ```bash
   python lab/eval.py
   ```

4. **Answer Queries**:
   ```bash
   python lab/rag_answer.py
   ```

## Data

The `lab/data/docs/` directory contains several documents that the RAG agent uses for retrieval. These include:
- Access Control SOP
- HR Leave Policy
- IT Helpdesk FAQ
- Policy Refund (v4)
- SLA P1 2026

## Notes

- Ensure that the Chroma database (`chroma_db/chroma.sqlite3`) is properly initialized before running the scripts.
- Refer to `lab/SCORING.md` for evaluation criteria.

## License

This repository is for educational purposes only. Please contact the course instructor for permissions and usage guidelines.
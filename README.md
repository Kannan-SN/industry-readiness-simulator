Industry-Readiness Combat Simulator
🎯 Project Overview
The Industry-Readiness Combat Simulator is an AI-powered platform that helps final-year students assess their job readiness through realistic industry scenarios. The system uses 6 specialized AI agents working together to generate scenarios, evaluate responses, identify skill gaps, and recommend personalized training paths.
🏗️ System Architecture
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (React + shadcn/ui)                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │   File Upload   │  │ Scenario Select │  │ Results Display │             │
│  │   Component     │  │   Component     │  │   Component     │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │ HTTP API Calls
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BACKEND (Python + FastAPI)                         │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    AI AGENTS ORCHESTRATION                          │   │
│  │                         (CrewAI)                                    │   │
│  │                                                                     │   │
│  │  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐      │   │
│  │  │   Scenario    │    │   Challenge   │    │   Response    │      │   │
│  │  │  Generator    │────▶   Presenter   │────▶  Collector    │      │   │
│  │  │    Agent      │    │     Agent     │    │     Agent     │      │   │
│  │  │  (RAG-enabled)│    │               │    │               │      │   │
│  │  └───────────────┘    └───────────────┘    └───────────────┘      │   │
│  │           │                                         │              │   │
│  │           ▼                                         ▼              │   │
│  │  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐      │   │
│  │  │   Training    │    │      Gap      │    │  Evaluation   │      │   │
│  │  │ Recommender   │◀───│   Diagnosis   │◀───│     Agent     │      │   │
│  │  │    Agent      │    │     Agent     │    │               │      │   │
│  │  │  (RAG-enabled)│    │               │    │               │      │   │
│  │  └───────────────┘    └───────────────┘    └───────────────┘      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                       │
│                                    ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                          LLM SERVICE                                │   │
│  │                      (Gemini-1.5-flash)                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │ Vector Search & Storage
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        WEAVIATE CLOUD DATABASE                             │
│                                                                             │
│  ┌─────────────────┐              ┌─────────────────┐                      │
│  │   Scenarios     │              │ Training        │                      │
│  │   Collection    │              │ Resources       │                      │
│  │   (Vector       │              │ Collection      │                      │
│  │   Embeddings)   │              │ (Vector         │                      │
│  └─────────────────┘              │ Embeddings)     │                      │
│                                   └─────────────────┘                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ▲
                                    │ CSV Data Input
┌─────────────────────────────────────────────────────────────────────────────┐
│                            CSV DATA FILES                                  │
│                                                                             │
│  ┌─────────────────┐              ┌─────────────────┐                      │
│  │   scenarios.csv │              │   training_     │                      │
│  │                 │              │   resources.csv │                      │
│  │   - role        │              │   - title       │                      │
│  │   - title       │              │   - type        │                      │
│  │   - task        │              │   - description │                      │
│  │   - difficulty  │              │   - url         │                      │
│  │   - context     │              │   - skills      │                      │
│  └─────────────────┘              └─────────────────┘                      │
└─────────────────────────────────────────────────────────────────────────────┘
🤖 AI Agents Architecture
Agent 1: Scenario Generator Agent (RAG-enabled)
File: backend/agents/scenario_generator_agent.py
Purpose: Creates realistic job scenarios from industry knowledge base
What it does:

Receives Input: Student role (frontend/backend/data_analyst/fullstack) + skill level
RAG Search: Queries Weaviate Cloud for relevant industry scenarios
LLM Generation: Uses Gemini to create new scenarios based on retrieved context
Output: 3 personalized scenarios with task descriptions, requirements, and success criteria

Process Flow:
Student Profile → RAG Search → Context Retrieval → LLM Generation → Scenario Creation
Example Output:
json{
  "id": "uuid-123",
  "role": "frontend",
  "title": "E-commerce Product Page",
  "task": "Create a responsive product page with add to cart functionality",
  "requirements": ["React components", "Responsive design", "State management"],
  "deliverables": ["Working product page", "Mobile-responsive design"],
  "criteria": ["Code quality", "User experience", "Performance"],
  "difficulty": "beginner"
}

Agent 2: Challenge Presenter Agent
File: backend/agents/challenge_presenter_agent.py
Purpose: Adapts scenarios to match student skill level and requirements
What it does:

Receives Input: Base scenario + student profile (skill level, role)
Complexity Adaptation: Adjusts difficulty based on beginner/intermediate/advanced level
Constraint Setting: Defines time limits and resource constraints
Instruction Generation: Creates specific, actionable instructions
Output: Customized challenge with adapted requirements

Adaptation Logic:

Beginner: Step-by-step guidance, 2-hour time limit, basic requirements
Intermediate: Some guidance, 1.5-hour time limit, additional requirements
Advanced: Minimal guidance, 1-hour time limit, complex optimization requirements

Example Output:
json{
  "scenario_id": "uuid-123",
  "adapted_task": "Build a simple product page using React hooks",
  "complexity_level": "beginner",
  "constraints": ["Step-by-step guidance provided", "Basic requirements only"],
  "instructions": "Create functional components, use useState for cart management",
  "time_limit": "2 hours"
}

Agent 3: Response Collector Agent
File: backend/agents/response_collector_agent.py
Purpose: Collects and validates student submissions
What it does:

Input Processing: Receives student responses (code, documents, files)
Type Detection: Automatically determines response type (code/document/design)
Validation: Checks content integrity and completeness
Content Analysis: Generates statistics (word count, code complexity, etc.)
Output: Structured, validated response data ready for evaluation

Validation Checks:

Content Length: Minimum character/word requirements
File Integrity: Ensures uploaded files are not corrupted
Type Consistency: Validates response matches expected format
Completeness: Checks all required fields are provided

Example Output:
json{
  "id": "response-456",
  "student_id": "student-123",
  "response_type": "code",
  "content": "function ProductPage() { ... }",
  "content_stats": {
    "word_count": 150,
    "function_count": 3,
    "has_imports": true
  },
  "validation": {"valid": true, "message": "Content validated successfully"}
}

Agent 4: LLM Evaluation Agent
File: backend/agents/evaluation_agent.py
Purpose: Evaluates student responses using predefined rubrics
What it does:

Input Analysis: Receives student response + original scenario requirements
Rubric Application: Evaluates against 4 criteria (25 points each):

Clarity: Code readability, documentation quality
Relevance: Alignment with task requirements
Correctness: Functional accuracy, error handling
Scalability: Performance considerations, design patterns


LLM Scoring: Uses Gemini to provide detailed scores and feedback
Grade Calculation: Converts scores to letter grades (A-F)
Output: Comprehensive evaluation with detailed feedback

Scoring System:

90-100: Grade A (Excellent)
80-89: Grade B (Good)
70-79: Grade C (Satisfactory)
60-69: Grade D (Needs Improvement)
0-59: Grade F (Unsatisfactory)

Example Output:
json{
  "response_id": "response-456",
  "scores": {
    "clarity": 22,
    "relevance": 20,
    "correctness": 18,
    "scalability": 15
  },
  "feedback": {
    "clarity": "Code is well-structured with good variable names",
    "correctness": "Missing error handling for edge cases"
  },
  "total_score": 75,
  "grade": "C"
}

Agent 5: Gap Diagnosis Agent
File: backend/agents/gap_diagnosis_agent.py
Purpose: Identifies specific skill gaps and areas for improvement
What it does:

Input Analysis: Evaluation results + response content analysis
Gap Categorization: Identifies gaps in three categories:

Technical Gaps: Implementation skills, technology knowledge
Conceptual Gaps: Understanding of principles and concepts
Process Gaps: Methodology, documentation, best practices


Priority Assessment: Determines which gaps are most critical
Urgency Calculation: Sets improvement urgency based on overall score
Output: Detailed gap analysis with prioritized improvement areas

Gap Detection Logic:

Score < 18/25: Indicates significant gap in that area
Response Analysis: Code structure, documentation quality
Pattern Recognition: Common mistakes and missing elements

Example Output:
json{
  "evaluation_id": "eval-789",
  "technical_gaps": ["Error handling", "Performance optimization"],
  "conceptual_gaps": ["Component lifecycle", "State management patterns"],
  "process_gaps": ["Code documentation", "Testing practices"],
  "improvement_urgency": "High - Significant improvement needed",
  "priority_areas": ["Conceptual understanding needs improvement"]
}

Agent 6: Training Recommender Agent (RAG-enabled)
File: backend/agents/training_recommender_agent.py
Purpose: Recommends personalized learning resources based on identified gaps
What it does:

Gap Analysis Input: Receives categorized skill gaps from diagnosis agent
RAG Resource Search: Queries Weaviate Cloud for relevant training materials
Resource Categorization: Organizes by priority and type:

Immediate: Critical skills needing urgent attention
Foundational: Core concepts and understanding
Practical: Hands-on projects and exercises
Advanced: Enhancement and optimization skills


Learning Path Creation: Structures resources into progressive phases
Duration Estimation: Calculates time needed for improvement
Output: Complete personalized learning roadmap

Learning Path Structure:

Phase 1: Critical Skills (1-2 weeks)
Phase 2: Foundation Building (2-3 weeks)
Phase 3: Practical Application (2-4 weeks)
Phase 4: Advanced Development (3-4 weeks)

Example Output:
json{
  "gap_analysis_id": "gap-789",
  "learning_path": [
    {
      "phase": 1,
      "title": "Critical Skills Development",
      "duration": "1-2 weeks",
      "resources": [
        {
          "title": "React Error Handling",
          "type": "tutorial",
          "description": "Learn proper error boundaries"
        }
      ]
    }
  ],
  "estimated_duration": "4-6 weeks",
  "urgency": "High"
}
📊 Data Flow Process
Complete Simulation Workflow:
1. Student Profile Input
   ↓
2. CSV Data Upload (Scenarios + Training Resources)
   ↓
3. Scenario Generator Agent (RAG Search + LLM Generation)
   ↓
4. Challenge Presenter Agent (Difficulty Adaptation)
   ↓
5. Student Response Submission
   ↓
6. Response Collector Agent (Validation + Analysis)
   ↓
7. Evaluation Agent (Rubric-based Scoring)
   ↓
8. Gap Diagnosis Agent (Skill Gap Identification)
   ↓
9. Training Recommender Agent (RAG-based Recommendations)
   ↓
10. Results Dashboard Display
Agent Interaction Flow:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CSV Upload    │───▶│  Vector Store   │───▶│ RAG-enabled     │
│   (Scenarios &  │    │   (Weaviate)    │    │ Agents (1 & 6)  │
│   Resources)    │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Gemini LLM    │◀───│  Agent Pipeline │◀───│  Student Input  │
│   (Processing)  │    │  (CrewAI)       │    │  (Profile +     │
│                 │    │                 │    │   Response)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│  Evaluation &   │    │   Training      │
│  Gap Analysis   │    │ Recommendations │
│                 │    │                 │
└─────────────────┘    └─────────────────┘
🗂️ Project Structure
industry-readiness-simulator/
├── README.md                          # This file
├── .env                              # Environment variables
├── start.sh                          # Startup script
│
├── frontend/                         # React Application
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/                   # shadcn/ui components
│   │   │   ├── FileUpload.jsx        # CSV upload interface
│   │   │   ├── ScenarioSelector.jsx  # Student profile & scenario selection
│   │   │   ├── ResponseSubmission.jsx # Solution submission form
│   │   │   └── ResultsDashboard.jsx  # Results display with recommendations
│   │   ├── pages/
│   │   │   ├── Home.jsx              # Landing page
│   │   │   └── Simulator.jsx         # Main assessment interface
│   │   ├── hooks/
│   │   │   └── useApi.js             # API integration hooks
│   │   ├── utils/
│   │   │   └── api.js                # API client
│   │   ├── App.jsx                   # Main app component
│   │   └── main.jsx                  # Entry point
│   ├── package.json
│   └── vite.config.js
│
├── backend/                          # Python Backend
│   ├── agents/                       # AI Agents
│   │   ├── scenario_generator_agent.py    # Agent 1: Scenario generation
│   │   ├── challenge_presenter_agent.py   # Agent 2: Challenge adaptation
│   │   ├── response_collector_agent.py    # Agent 3: Response validation
│   │   ├── evaluation_agent.py            # Agent 4: LLM evaluation
│   │   ├── gap_diagnosis_agent.py         # Agent 5: Gap analysis
│   │   └── training_recommender_agent.py  # Agent 6: Training recommendations
│   │
│   ├── crew/                         # CrewAI Orchestration
│   │   ├── simulator_crew.py         # Main orchestration logic
│   │   └── tasks.py                  # Task definitions
│   │
│   ├── database/                     # Weaviate Integration
│   │   ├── weaviate_client.py        # Cloud connection
│   │   ├── vector_store.py           # Vector operations
│   │   └── data_loader.py            # CSV processing
│   │
│   ├── models/                       # Data Models
│   │   ├── scenario.py               # Scenario data structures
│   │   ├── student.py                # Student profiles
│   │   ├── response.py               # Response & evaluation models
│   │   └── evaluation.py             # Evaluation results
│   │
│   ├── services/                     # Business Logic
│   │   ├── csv_processor.py          # CSV file processing
│   │   ├── llm_service.py            # Gemini LLM integration
│   │   └── orchestrator.py           # Agent coordination
│   │
│   ├── api/                          # FastAPI Routes
│   │   ├── main.py                   # Main API application
│   │   └── routes/                   # API endpoints
│   │
│   ├── config/                       # Configuration
│   │   ├── settings.py               # Environment settings
│   │   └── prompts.py                # LLM prompts
│   │
│   ├── data/                         # CSV Data Storage
│   │   ├── scenarios/                # Scenario CSV files
│   │   ├── students/                 # Student data (optional)
│   │   └── training_resources/       # Training resource CSVs
│   │
│   ├── requirements.txt              # Python dependencies
│   └── main.py                       # Backend entry point
│
└── csv_templates/                    # Sample CSV files (see below)
    ├── scenarios.csv
    ├── training_resources.csv
    └── students.csv
📋 CSV File Requirements
1. scenarios.csv
Purpose: Contains job scenarios for different roles and difficulty levels
Required Columns:

role: Job role (frontend, backend, data_analyst, fullstack)
title: Short scenario title
task: Detailed task description
difficulty: Skill level (beginner, intermediate, advanced)
context: Additional context or background information

2. training_resources.csv
Purpose: Contains learning resources for skill improvement
Required Columns:

title: Resource title
type: Resource type (course, tutorial, project, documentation, book)
description: Brief description of the resource
url: Link to the resource (use # for placeholder)
skills: Comma-separated skills covered

3. students.csv (Optional)
Purpose: Pre-defined student profiles for testing
Required Columns:

id: Unique student identifier
name: Student name
role: Preferred job role
skill_level: Current skill level
email: Contact email (optional)

🚀 Installation & Setup
Prerequisites

Python 3.12.7
Node.js 18+
Git
VS Code (recommended)

Environment Setup

Clone or create the project structure:

bashmkdir industry-readiness-simulator
cd industry-readiness-simulator

Set up environment variables:
Create .env file in project root:

envGOOGLE_API_KEY=your_gemini_api_key_here
WEAVIATE_URL=https://your-cluster.weaviate.cloud
WEAVIATE_API_KEY=your_weaviate_api_key
CORS_ORIGINS=http://localhost:5173

Backend setup:

bashcd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

Frontend setup:

bashcd frontend
npm install
Starting the Application
Option 1: Using startup script
bashchmod +x start.sh
./start.sh
Option 2: Manual startup
bash# Terminal 1: Backend
cd backend
source venv/bin/activate
python main.py

# Terminal 2: Frontend  
cd frontend
npm run dev
Accessing the Application

Frontend: http://localhost:5173
Backend API: http://localhost:8000
API Documentation: http://localhost:8000/docs

📄 CSV Templates
scenarios.csv
csvrole,title,task,difficulty,context
frontend,E-commerce Product Page,Create a responsive product page with add to cart functionality,beginner,Build a product display page for an online store with shopping cart integration
frontend,React Dashboard,Build a data visualization dashboard using React and charts,intermediate,Create an analytics dashboard for business metrics and KPI tracking
frontend,Advanced UI Library,Develop a reusable component library with TypeScript,advanced,Build scalable component system for enterprise applications
backend,REST API for Blog,Design and implement a REST API for a blogging platform,beginner,Build backend services for a content management system with CRUD operations
backend,Microservices Architecture,Design a microservices system for an e-commerce platform,advanced,Scale backend services for high-traffic applications with distributed architecture
backend,Authentication System,Implement secure user authentication and authorization,intermediate,Build secure login system with JWT tokens and role-based access control
data_analyst,Sales Data Analysis,Analyze quarterly sales data and identify trends,beginner,Examine business performance using statistical methods and data visualization
data_analyst,Customer Segmentation,Perform customer segmentation using machine learning,intermediate,Use clustering algorithms to identify customer groups for targeted marketing
data_analyst,Predictive Analytics,Build predictive models for business forecasting,advanced,Create machine learning models for revenue prediction and risk assessment
fullstack,Social Media App,Build a complete social media application,advanced,Create end-to-end social networking platform with real-time features
fullstack,Task Management System,Develop a project management tool,intermediate,Build collaborative workspace with task tracking and team features
fullstack,E-learning Platform,Create an online education platform,advanced,Develop comprehensive learning management system with video streaming
training_resources.csv
csvtitle,type,description,url,skills
React Fundamentals Course,course,Learn React basics from scratch with hands-on projects,#,React JavaScript frontend components
Node.js Backend Development,course,Complete backend development with Node.js and Express,#,Node.js backend API Express JavaScript
Python for Data Analysis,course,Data analysis using pandas numpy and matplotlib,#,Python data analysis pandas numpy matplotlib
SQL Database Design,tutorial,Learn database design principles and optimization,#,SQL database design normalization optimization
Git Version Control,tutorial,Master Git for version control and collaboration,#,Git version control collaboration branching
JavaScript ES6+ Features,tutorial,Modern JavaScript programming with latest features,#,JavaScript ES6 programming async promises
REST API Best Practices,documentation,Guidelines for designing scalable REST APIs,#,API REST backend design HTTP methods
React Portfolio Project,project,Build a professional portfolio website with React,#,React project portfolio components styling
Data Visualization with D3,course,Create interactive charts and graphs with D3.js,#,D3 visualization charts SVG JavaScript
Docker Containerization,tutorial,Learn Docker for application deployment,#,Docker containers deployment DevOps
MongoDB Database,course,NoSQL database design and operations with MongoDB,#,MongoDB NoSQL database aggregation indexing
Python Machine Learning,course,Machine learning with scikit-learn and TensorFlow,#,Python machine learning scikit-learn TensorFlow
TypeScript Fundamentals,tutorial,Add type safety to JavaScript applications,#,TypeScript JavaScript types interfaces
AWS Cloud Services,course,Cloud deployment and services with Amazon Web Services,#,AWS cloud deployment serverless S3
CSS Grid and Flexbox,tutorial,Modern CSS layout techniques for responsive design,#,CSS layout responsive design Grid Flexbox
Redux State Management,tutorial,Manage application state with Redux and Redux Toolkit,#,Redux state management React JavaScript
Express.js Framework,tutorial,Build web applications with Express.js framework,#,Express.js Node.js backend middleware routing
Pandas Data Processing,tutorial,Data manipulation and analysis with pandas library,#,pandas Python data processing cleaning analysis
GraphQL API Development,course,Build flexible APIs with GraphQL and Apollo,#,GraphQL API backend Apollo Node.js
Jupyter Notebooks,tutorial,Interactive data science with Jupyter notebooks,#,Jupyter Python data science notebooks analysis
students.csv (Optional)
csvid,name,role,skill_level,email
1,John Smith,frontend,beginner,john.smith@example.com
2,Sarah Johnson,backend,intermediate,sarah.j@example.com
3,Mike Chen,data_analyst,beginner,mike.chen@example.com
4,Emily Davis,fullstack,advanced,emily.d@example.com
5,Alex Rodriguez,frontend,intermediate,alex.r@example.com
6,Lisa Wang,backend,advanced,lisa.wang@example.com
7,David Brown,data_analyst,intermediate,david.b@example.com
8,Jessica Lee,fullstack,beginner,jessica.lee@example.com
🔧 Configuration
Environment Variables

GOOGLE_API_KEY: Your Google Gemini API key
WEAVIATE_URL: Your Weaviate Cloud cluster URL
WEAVIATE_API_KEY: Your Weaviate Cloud API key
CORS_ORIGINS: Allowed frontend origins (comma-separated)

Customization Options

Add new roles: Modify role enums in models/scenario.py
Adjust scoring rubrics: Update prompts in config/prompts.py
Modify evaluation criteria: Change scoring logic in evaluation_agent.py
Add new resource types: Extend training resource categories

🧪 Testing
Quick Test Workflow

Start the application
Upload sample CSV files (provided above)
Create a student profile:

Name: Test Student
Role: Frontend
Skill Level: Beginner


Generate scenarios and select one
Submit a sample response:
javascriptfunction ProductPage() {
  const [cartItems, setCartItems] = useState([]);
  
  const addToCart = (product) => {
    setCartItems([...cartItems, product]);
  };
  
  return (
    <div className="product-page">
      <h1>Product Title</h1>
      <button onClick={() => addToCart(product)}>
        Add to Cart
      </button>
    </div>
  );
}

View evaluation results and training recommendations

Expected Results

Evaluation scores for clarity, relevance, correctness, scalability
Skill gap identification in technical, conceptual, and process areas
Personalized learning path with 4 phases of improvement
Resource recommendations tailored to identified gaps

🔍 Troubleshooting
Common Issues

Weaviate Connection Failed

Check your cloud URL and API key
Verify internet connection
Ensure Weaviate Cloud instance is active


Gemini API Errors

Verify your Google API key is correct
Check API quotas and billing
Ensure Gemini API is enabled


CSV Upload Issues

Verify CSV format matches required columns
Check for proper encoding (UTF-8)
Ensure no empty required fields


Agent Processing Errors

Check backend logs for specific errors
Verify all environment variables are set
Ensure sufficient API quotas



Debug Mode
Enable detailed logging by setting log level in main.py:
pythonlogging.basicConfig(level=logging.DEBUG)
📈 Performance Considerations

Vector Search: Optimized for cloud infrastructure
Batch Processing: Efficient CSV uploads with batch operations
Caching: LLM responses cached to reduce API calls
Error Recovery: Graceful fallbacks for failed agent operations
Scalability: Designed for multiple concurrent users

🔒 Security

API Key Management: Environment variables for sensitive data
Input Validation: Comprehensive validation for all user inputs
Error Handling: Secure error messages without exposing internals
CORS Configuration: Controlled access from specified origins

🤝 Contributing
To extend the system:

Add new agents: Follow the existing agent pattern
Modify prompts: Update LLM prompts in config/prompts.py
Extend data models: Add new fields to Pydantic models
Add new evaluation criteria: Modify rubrics and scoring logic

📞 Support
For issues or questions:

Check the troubleshooting section
Review backend logs for error details
Verify CSV file formats
Ensure all environment variables are correctly set


This system provides a complete AI-powered assessment platform that can be easily customized and extended for various educational and professional development needs. The modular architecture ensures maintainability while the CSV-driven approach provides flexibility for different use cases.
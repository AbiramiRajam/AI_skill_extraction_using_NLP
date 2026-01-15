# ---------------------- INSTALLATION ---------------------- #
# To install required packages, run the following commands:
# pip install streamlit
# pip install pdfplumber
# pip install python-docx
# pip install spacy
# python -m spacy download en_core_web_sm
# ---------------------- IMPORTS ---------------------- #
import streamlit as st
import pdfplumber
import docx
import spacy
from spacy.matcher import PhraseMatcher
from collections import defaultdict

st.set_page_config(layout="wide")

# ---------------------- STREAMLIT SETUP ---------------------- #

import streamlit as st
import pdfplumber
import docx

st.title("AI Job Skill Analyzer ")

# Initialize session state
if "job_description_text" not in st.session_state:
    st.session_state.job_description_text = ""

# ---------------------- INPUT METHOD ---------------------- #
input_option = st.radio(
    "Choose input method:",
    ["Paste Text", "Upload File (PDF/DOCX)"],
    horizontal=True
)

# ---------------------- TWO COLUMNS ---------------------- #
col1, col2 = st.columns(2)

# ---------------------- LEFT COLUMN (INPUT) ---------------------- #
with col1:
    st.subheader("Job Overview")

    if input_option == "Paste Text":
        pasted_text = st.text_area(
            " ",
            height=300,
            key="input_text_area",              # unique key
            label_visibility="collapsed"
        )

        if pasted_text:
            st.session_state.job_description_text = pasted_text

    else:
        uploaded_file = st.file_uploader(
            "Upload Job Description File",
            type=["pdf", "docx"]
        )

        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                with pdfplumber.open(uploaded_file) as pdf:
                    pages = [
                        page.extract_text()
                        for page in pdf.pages
                        if page.extract_text()
                    ]
                    st.session_state.job_description_text = "\n".join(pages)

            elif uploaded_file.type == (
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ):
                doc = docx.Document(uploaded_file)
                st.session_state.job_description_text = "\n".join(
                    para.text for para in doc.paragraphs
                )

# ---------------------- RIGHT COLUMN (OUTPUT) ---------------------- #
with col2:
    st.subheader("Skill Dashboard")

    st.text_area(
        " ",
        value=st.session_state.job_description_text,
        height=300,
        key="output_text_area",                 # ✅ unique key
        label_visibility="collapsed",
        disabled=True                            # optional (read-only)
    )


# ---------------------- TECH STACK & SOFT SKILLS (DEDUPED) ---------------------- #
TECH_STACK = {

    "minimum_qualifications": {
        "experience": {
            "min_years": None,   # dynamic input
            "domain": None       # dynamic input
        }
    },

    "api_integrations": [
        "api integration", "apis", "rest api", "restful api", "soap api", "graphql",
        "web services", "microservices", "json", "xml",
        "oauth", "oauth2", "openid connect", "jwt", "swagger", "openapi",
        "postman", "api gateway", "aws api gateway", "azure api management",
        "mule api", "mulesoft", "boomi", "kafka rest proxy"
    ],

    "programming_languages": [
        "python", "java", "scala", "r", "c", "c++", "c#", "go",
        "javascript", "typescript", "bash", "powershell",
        "sql", "pl/sql", "tsql", "nosql"
    ],

    "databases": [
        "mysql", "postgresql", "oracle", "sql server", "sqlite",
        "mongodb", "cassandra", "redis", "couchbase"
    ],

    "data_warehouses": [
        "snowflake", "redshift", "bigquery", "azure synapse",
        "teradata", "oracle exadata", "greenplum"
    ],

    "bi_reporting_tools": [
        "power bi", "tableau", "qlik", "qlik sense", "qlikview",
        "cognos", "sap businessobjects", "looker", "microstrategy",
        "sisense", "domo", "thoughtspot", "tibco spotfire",
        "oracle analytics cloud", "ibm planning analytics", "pentaho",
        "yellowfin bi", "mode analytics", "chartio", "klipfolio",
        "zoho analytics", "metabase", "redash", "hevo analytics",
        "datawrapper", "gooddata", "grow.com", "google data studio",
        "databricks dashboards", "excel pivot tables", "excel charts", "excel dashboards",
        "ssrs", "ssis", "sap analytics cloud", "tableau desktop", "tableau server", "tableau online"
    ],

    "etl_tools": [
        "informatica", "talend", "ab initio", "ssis", "sap bods", "sap data services",
        "matillion", "fivetran", "stitch", "airflow", "prefect", "luigi",
        "azure data factory", "aws glue", "SnapLogic", "dbt",
        "data warehousing concepts", "star schema design", "snowflake schema design",
        "OLAP design", "OLTP design", "ETL/ELT design patterns", "data modeling",
        "dimensional modeling", "data marts", "fact tables", "dimension tables"
    ],

    "data_migration_tools": [
        "aws dms", "azure database migration service", "oracle golden gate", "attunity",
        "flyway", "liquibase", "sqoop", "talend data migration", "informatica data migration",
        "supporting large enterprise databases", "high availability and reliability",
        "database performance tuning", "backup and recovery strategies",
        "database monitoring and optimization", "transaction management",
        "indexing strategies", "query optimization"
    ],

    "sap_functional": [
        "sap fico", "sap mm", "sap sd", "sap pp", "sap hr", "sap hcm", "sap wm", "sap qm",
        "sap crm", "sap bw", "B4HANA", "SAP Native HANA", "sap bw/4hana"
    ],

    "sap_technical": [
        "sap abap", "sap hana", "sap s/4hana", "sap ui5", "sap fiori", "sap netweaver",
        "sap basis", "sap datasphere", "bw/4hana", "SAP FS-CD", "OData Services",
        "BAPI Services", "ABAP CDS", "AMDP", "user exists", "BADIs",
        "Enterprise Management", "Finance", "FICA", "Enterprise WM"
    ],

    "cloud_platforms": [
        "aws", "azure", "gcp", "oracle cloud", "ibm cloud",
        "azure sql", "azure sql managed instance", "sql server on azure vm",
        "cloud database deployments", "cloud data security",
        "azure monitoring and diagnostics", "azure backup and recovery"
    ],

    "devops_tools": [
        # CI/CD & Automation
        "jenkins", "gitlab ci", "github actions", "bitbucket pipelines",
        "circleci", "travis ci", "azure devops pipelines", "tekton", "argo cd", "spinnaker",
        # Source Control
        "git", "github", "gitlab", "bitbucket", "svn", "mercurial",
        # Infrastructure as Code
        "terraform", "cloudformation", "pulumi", "ansible", "chef", "puppet", "saltstack",
        # Containerization & Orchestration
        "docker", "docker compose", "podman", "buildah", "kaniko",
        "kubernetes", "openshift", "eks", "aks", "gke", "rancher", "k3s", "helm", "istio",
        # Monitoring & Logging
        "prometheus", "grafana", "datadog", "new relic", "splunk", "elk stack",
        "elastic stack", "opensearch", "cloudwatch", "azure monitor", "gcp operations suite",
        "nagios", "zabbix",
        # Artifact / Package Management
        "nexus", "artifactory", "aws codeartifact", "jfrog",
        # Collaboration / ChatOps
        "slack", "microsoft teams", "mattermost", "pagerduty", "opsgenie",
        # Scripting & Automation
        "bash scripting", "powershell", "python scripts", "shell scripting", "cron jobs",
        "ksh", "zsh", "awk", "sed", "perl",
        # Security / Testing
        "sonarqube", "checkmarx", "fortify", "trivy", "aqua security", "snyk", "dependabot"
    ],

    "monitoring_observability": [
        "prometheus", "grafana", "datadog", "new relic", "splunk",
        "elastic stack", "opensearch", "cloudwatch", "azure monitor", "gcp operations"
    ],

    "containerization_orchestration": [
        "docker", "docker compose", "kubernetes", "openshift", "eks", "aks", "gke"
    ],

    "ml_ai": [
        "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
        "scikit-learn", "xgboost", "nlp", "computer vision", "mlflow", "kubeflow"
    ],

    "scripting_tools": [
        "bash scripting", "shell scripting", "ksh", "zsh", "awk", "sed", "perl",
        "powershell", "python scripts", "sql scripts", "pl/sql scripts", "tsql scripts",
        "cron jobs", "linux admin scripts", "windows admin scripts",
        "sapstart scripts", "sapcontrol scripts", "hana cli scripts", "hdbsql",
        "vcs cluster scripts", "pacemaker scripts", "sbd fencing scripts",
        "backup automation scripts", "unix"
    ],

    "document_tools": [
        "microsoft word", "microsoft excel", "microsoft powerpoint",
        "google documents", "google sheets", "google slides",
        "notion", "dropbox paper", "zoho docs", "confluence pages",
        "sharepoint", "coda", "quip", "evernote"
    ],

    "management_tools": [
        "jira", "asana", "trello", "monday.com",
        "clickup", "ms project", "confluence", "smartsheet",
        "wrike", "teamwork", "basecamp", "notion project management"
    ],

    "compliance_tools": [
        "HIPAA", "GDPR", "SOC 1", "SOC 2", "SOC 3", "ISO 27001", "ISO 9001",
        "PCI-DSS", "ITAR", "FERPA", "FISMA", "NIST", "COBIT", "SOX",
        "CSA STAR", "CCPA"
    ],

    "enterprise_tools": [
        "agpa technical tools", "vcs", "pacemaker", "sbd", "third-party admin tools",
        "ticketing systems", "service desk tools", "monitoring dashboards"
    ],

    "project_management_methodologies": [
        "agile", "scrum", "kanban", "waterfall", "lean",
        "six sigma", "prince2", "xp (extreme programming)",
        "scrum ban", "crystal", "dynamic systems development method (DSDM)",
        "rational unified process (RUP)"
    ],

    "soft_skills": [
        "communication", "analytical thinking", "problem solving",
        "teamwork", "stakeholder management", "presentation",
        "training", "documentation"
    ]
}

ALIASES = {
    "node.js": "node",
    "powerbi": "power bi",
    "bw4hana": "bw/4hana",
    "postgres": "postgresql",
    "js": "javascript",
    "c plus plus": "c++"
}


# ---------------------- NORMALIZE FUNCTION ---------------------- #
def normalize(text):
    text = text.lower()
    for k, v in ALIASES.items():
        text = text.replace(k, v)
    return text

# ---------------------- NLP SETUP ---------------------- #
nlp = spacy.load("en_core_web_sm")
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")  # create matcher once

def build_matcher(tech_stack):
    global matcher
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")  # recreate matcher to reset patterns
    for category, terms in tech_stack.items():
        patterns = [nlp.make_doc(term) for term in terms]
        matcher.add(category, patterns)

# Build matcher once
build_matcher(TECH_STACK)


# ---------------------- EXTRACTION FUNCTION ---------------------- #
def extract_tech(text):
    text = normalize(text)
    doc = nlp(text)
    matches = matcher(doc)
    results = defaultdict(lambda: defaultdict(int))
    for match_id, start, end in matches:
        category = nlp.vocab.strings[match_id]
        term = doc[start:end].text.lower()
        results[category][term] += 1
    return results

# ---------------------- STREAMLIT EXTRACTION ---------------------- #
job_description_text = st.session_state.get("job_description_text", "")

if job_description_text.strip():
    output = extract_tech(job_description_text)
    st.subheader("Extracted Tech Stack & Skills")

    # Determine number of columns dynamically 
    categories = list(output.keys())

    # Bring minimum_qualifications first if it exists
    if "minimum_qualifications" in categories:
        categories.remove("minimum_qualifications")
        categories = ["minimum_qualifications"] + categories

    n_cols = 3
    cols = st.columns(n_cols)

    # Display each category in a column
    for idx, category in enumerate(categories):
        with cols[idx % n_cols]:
            st.markdown(f"**{category.replace('_',' ').title()}**")
            terms = output[category]
            for term, count in terms.items():
                st.write(f"- {term} ({count})")
else:
    st.info("No job description text available for extraction.")




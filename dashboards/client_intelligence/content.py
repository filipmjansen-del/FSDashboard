"""Manually curated, non-production content for the AL Sydbank MVP pilot."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceMetadata:
    publisher: str
    title: str
    publication_date: str
    source_type: str
    page_reference: str | None = None
    url: str | None = None


@dataclass(frozen=True)
class PilotContext:
    display_name: str
    pilot_label: str
    latest_reporting_label: str
    legal_entity_reference: str | None = None
    regnr: str | None = None


@dataclass(frozen=True)
class PilotItem:
    title: str
    detail: str
    information_type: str
    source: SourceMetadata
    period: str


@dataclass(frozen=True)
class CommercialHypothesis:
    title: str
    evidence: str
    observation: str
    potential_need: str
    thursday_relevance: str
    period: str
    sources: tuple[SourceMetadata, ...]
    validation_questions: tuple[str, ...]


PILOT_CONTEXT = PilotContext(
    display_name="AL Sydbank",
    pilot_label="AL Sydbank MVP pilot",
    latest_reporting_label="H1 2026",
    legal_entity_reference="bank:8079",
    regnr="8079",
)
H1_2026_SOURCE_TITLE = "Delårsrapport - 1. halvår 2026"
H1_2026_SOURCE_URL = "https://ml-eu.globenewswire.com/Resource/Download/c2791f30-e63c-466a-93a8-ec58739d267e"
H1_2026_PAGE_30_SOURCE = SourceMetadata(
    publisher="AL Sydbank A/S",
    title=H1_2026_SOURCE_TITLE,
    publication_date="26 August 2026",
    source_type="Official company reporting",
    page_reference="Page 30",
    url=H1_2026_SOURCE_URL,
)
H1_2026_PAGE_46_SOURCE = SourceMetadata(
    publisher="AL Sydbank A/S",
    title=H1_2026_SOURCE_TITLE,
    publication_date="26 August 2026",
    source_type="Official company reporting",
    page_reference="Page 46",
    url=H1_2026_SOURCE_URL,
)
H1_2026_HIGHLIGHTS_SOURCE = SourceMetadata(
    publisher="AL Sydbank A/S",
    title=H1_2026_SOURCE_TITLE,
    publication_date="26 August 2026",
    source_type="Official company reporting",
    url=H1_2026_SOURCE_URL,
)
THURSDAY_BENCHMARK_SOURCE = SourceMetadata(
    publisher="Thursday",
    title="Inspirationsdeck til AL Sydbank om DB v3.pdf",
    publication_date="September 2026",
    source_type="Thursday internal benchmark material",
)
THURSDAY_ACCOUNT_SOURCE = SourceMetadata(
    publisher="Thursday",
    title="Bank workshop / relationship material",
    publication_date="Current source set",
    source_type="Thursday internal account intelligence",
)
THURSDAY_ACTION_LOG_SOURCE = SourceMetadata(
    publisher="Thursday",
    title="Bank action log",
    publication_date="Current source set",
    source_type="Thursday internal account intelligence",
)
THURSDAY_CAPABILITY_SOURCE = SourceMetadata(
    publisher="Thursday",
    title="Thursday banking capability material",
    publication_date="Current source set",
    source_type="Thursday internal material",
)
CUSTOMER_PROPOSITION_SOURCE = SourceMetadata(
    publisher="AL Sydbank A/S", title="Farvel til gebyr", publication_date="September 2026",
    source_type="Official company news", url="https://www.al-sydbank.dk/nyt/farvel-til-gebyr",
)
MERGER_POSITIONING_SOURCE = SourceMetadata(
    publisher="AL Sydbank A/S", title="Fusionen til AL Sydbank er nu en realitet", publication_date="2026",
    source_type="Official company news", url="https://www.al-sydbank.dk/nyt/fusionen-til-al-sydbank-er-nu-en-realitet",
)
LARGER_BANK_SOURCE = SourceMetadata(
    publisher="AL Sydbank A/S", title="Vi vil skabe en større bank", publication_date="2026",
    source_type="Official company news", url="https://www.al-sydbank.dk/nyt/vi-vil-skabe-en-stoerre-bank",
)
ORGANISATION_SOURCE = SourceMetadata(
    publisher="AL Sydbank A/S", title="Organisation", publication_date="Current public organisation page",
    source_type="Official company information", url="https://www.al-sydbank.dk/om-os/organisation",
)

MERGER_FACTS = (
    PilotItem(
        "Integration costs",
        "H1 2026 integration costs related to the merger were reported as DKK 32m.",
        "Fact",
        H1_2026_PAGE_30_SOURCE,
        "H1 2026",
    ),
    PilotItem(
        "BEC exit compensation",
        "The reported integration costs primarily relate to BEC exit compensation.",
        "Fact",
        H1_2026_PAGE_30_SOURCE,
        "H1 2026",
    ),
    PilotItem(
        "Liquidity effect",
        "The merger was reported to have a positive liquidity effect of DKK 12,485m.",
        "Fact",
        H1_2026_PAGE_46_SOURCE,
        "H1 2026",
    ),
    PilotItem(
        "Acquisition goodwill",
        "Goodwill related to the acquisition was reported as DKK 7,689m.",
        "Fact",
        H1_2026_PAGE_46_SOURCE,
        "H1 2026",
    ),
    PilotItem(
        "Reported synergy context",
        "The report states that goodwill can partly be related to significant cost and capital synergies.",
        "Fact",
        H1_2026_PAGE_46_SOURCE,
        "H1 2026",
    ),
)

H1_2026_SNAPSHOT = (
    PilotItem("Result after tax", "DKK 1,761m", "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026"),
    PilotItem("ROTE after tax", "13.3%", "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026"),
    PilotItem("Bank loans", "DKK 143.7bn", "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026"),
    PilotItem("Deposits", "DKK 219.4bn", "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026"),
    PilotItem("CET1 ratio", "16.0%", "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026"),
    PilotItem("Employees", "3,888", "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026"),
)

H1_2026_PERFORMANCE_KPIS = H1_2026_SNAPSHOT[:5] + (
    PilotItem("Cost/income", "57.1%", "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026"),
    PilotItem("LCR", "279%", "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026"),
)

Q2_2026_MOMENTUM = (
    ("Result before tax", "DKK 1,043m", "DKK 1,274m"),
    ("Basis income", "DKK 2,925m", "DKK 2,996m"),
    ("Basis costs", "DKK 1,755m", "DKK 1,732m"),
    ("Result after tax", "DKK 803m", "DKK 958m"),
)

DOCUMENTED_AL_SYDBANK_SIGNALS = (
    PilotItem(
        "Integration", "AL Sydbank was created through the December 2025 merger of Sydbank, Arbejdernes Landsbank and Vestjysk Bank.",
        "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "December 2025",
    ),
    PilotItem(
        "Synergies", "DKK 175m cost synergies were realised in H1 2026; management states synergy work is progressing according to plan.",
        "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026",
    ),
    PilotItem(
        "Distribution footprint", "52 branches were consolidated in H1. 88 branches remain in Denmark and 3 in Germany, with presence retained in all towns where the bank was present at merger.",
        "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026",
    ),
    PilotItem(
        "Technology", "Bankdata transition is targeted for 2027. Management links the work to reduced complexity, customer-facing solutions and a scalable bank.",
        "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "2027 target",
    ),
    PilotItem(
        "Strategic ambition", "Management's stated ambition is to combine big-bank capabilities with local proximity.",
        "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026",
    ),
    PilotItem(
        "Commercial momentum", "Management reports positive development among private customers, particularly in housing and investment.",
        "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026",
    ),
    PilotItem(
        "Earnings outlook", "2026 result after tax is expected in the upper half of the DKK 3.5-4.0bn guidance range.",
        "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "2026 outlook",
    ),
)

WHAT_MATTERS_NOW = (
    PilotItem(
        "Integration execution", "DKK 175m cost synergies realised; 52 branches consolidated; 88 Danish branches remain; Bankdata migration preparation for 2027 continues.",
        "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026",
    ),
    PilotItem(
        "Customer and commercial momentum", "Management reports positive private-customer development in housing and investment, alongside an ambition to combine big-bank capabilities with local proximity.",
        "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026",
    ),
    PilotItem(
        "Earnings and outlook", "2026 result after tax is expected in the upper half of the DKK 3.5-4.0bn guidance range.",
        "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "2026 outlook",
    ),
)

THURSDAY_PERSPECTIVES = (
    PilotItem(
        "Service model and segmentation",
        "Danske Bank uses explicit service tiers and differentiated adviser models.",
        "Thursday perspective",
        THURSDAY_BENCHMARK_SOURCE,
        "September 2026",
    ),
    PilotItem(
        "Data-driven customer activation",
        "Thursday's benchmark highlights data-driven lead identification and proactive customer management.",
        "Thursday perspective",
        THURSDAY_BENCHMARK_SOURCE,
        "September 2026",
    ),
    PilotItem(
        "Capacity and skills routing",
        "Benchmark material describes routing work based on skills and available capacity.",
        "Thursday perspective",
        THURSDAY_BENCHMARK_SOURCE,
        "September 2026",
    ),
    PilotItem(
        "Industrialised AI",
        "Benchmark perspective focuses on common platforms, governance and process-level value rather than isolated AI use cases.",
        "Thursday perspective",
        THURSDAY_BENCHMARK_SOURCE,
        "September 2026",
    ),
)

CUSTOMER_PROPOSITION_SIGNAL = PilotItem(
    "Customer proposition", "AL Sydbank removed account and netbank fees for relevant private customers.",
    "Fact", CUSTOMER_PROPOSITION_SOURCE, "September 2026",
)
STRATEGIC_POSITIONING_SIGNAL = PilotItem(
    "Strategic positioning", "Public merger communication describes a broader offering, more specialist capabilities, stronger digital solutions, and a national/local distribution footprint.",
    "Fact", MERGER_POSITIONING_SOURCE, "2026",
)
PUBLIC_EXECUTIVES = (
    PilotItem("Mark Luscombe", "CEO", "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026"),
    PilotItem("Frank Mortensen", "Vice CEO", "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026"),
    PilotItem("Jørn Adam Møller", "Bank Director, CFO", "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026"),
    PilotItem("Stig Westergaard", "Bank Director, CRO", "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026"),
    PilotItem("Svend Randers", "Bank Director", "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026"),
    PilotItem("Peter Hupfeld", "Bank Director", "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026"),
    PilotItem("Gry Bandholm", "Bank Director", "Public fact", H1_2026_HIGHLIGHTS_SOURCE, "H1 2026"),
)
INTERNAL_ACCOUNT_MAPPING = (
    "Frank Mortensen", "Svend Randers", "Gry Bandholm", "Jørn Adam Møller",
)
RECENT_ACCOUNT_ACTIVITY = (
    PilotItem("Danske Bank benchmark / information process", "Svend Randers — completed.", "Thursday internal knowledge", THURSDAY_ACTION_LOG_SOURCE, "Recent account activity"),
    PilotItem("Meeting/action identified", "Jørn Adam Møller and Svend Randers.", "Thursday internal knowledge", THURSDAY_ACTION_LOG_SOURCE, "Current source set"),
    PilotItem("Meeting/action identified", "Frank Mortensen and Svend Randers.", "Thursday internal knowledge", THURSDAY_ACTION_LOG_SOURCE, "Current source set"),
    PilotItem("Credit-process dialogue", "AL Sydbank dialogue involving fusion / Bankdata context is ongoing.", "Thursday internal knowledge", THURSDAY_ACTION_LOG_SOURCE, "Current source set"),
)
THURSDAY_FOOTPRINT = (
    PilotItem("AL x Thursday Bankrapport", "Client-specific banking insight material.", "Thursday internal material", THURSDAY_ACCOUNT_SOURCE, "November 2025"),
    PilotItem("AL Sydbank / Danske Bank benchmark", "Benchmark of strategy, customer/service model, AI, IT and operating model.", "Thursday internal material", THURSDAY_BENCHMARK_SOURCE, "September 2026"),
    PilotItem("AL Markets reorganisation", "Prior Thursday assignment referenced in current Thursday capability material.", "Thursday internal material", THURSDAY_CAPABILITY_SOURCE, "Current source set"),
    PilotItem("Svend Randers benchmark dialogue", "Recent account activity using Danske Bank inspiration material.", "Thursday internal knowledge", THURSDAY_ACTION_LOG_SOURCE, "Recent account activity"),
)
THURSDAY_CAPABILITY_MAPPINGS = (
    PilotItem("Integration & operating model", "Current client signal: merger integration, branch consolidation and Bankdata preparation. Relevant Thursday capability: Organisationsanalyse & Design; Datadrevet forandringsledelse / Thursday Transformation Tracker.", "Thursday perspective", THURSDAY_CAPABILITY_SOURCE, "Current source set"),
    PilotItem("Service model & efficiency", "Current client signal: local proximity alongside scale and private-customer momentum. Relevant Thursday capability: Process Excellence; capacity management where relevant.", "Thursday perspective", THURSDAY_CAPABILITY_SOURCE, "Current source set"),
    PilotItem("Technology & migration", "Current client signal: Bankdata transition targeted for 2027. Relevant Thursday capability: EA / architecture decision support; IT Delivery Lead.", "Thursday perspective", THURSDAY_CAPABILITY_SOURCE, "Current source set"),
    PilotItem("AI & data", "Current client signal: management focus on customer-facing solutions and a scalable bank. Relevant Thursday capability: AI adoption / operating model.", "Thursday perspective", THURSDAY_CAPABILITY_SOURCE, "Current source set"),
)

PERFORMANCE_GUIDANCE = PilotItem(
    "Existing Databank capability",
    "Use Bank → Bank Analyst View for AL Sydbank financial performance and peer benchmarking; this MVP does not create a parallel analytics engine.",
    "MVP guidance",
    SourceMetadata(
        publisher="Databank",
        title="Bank Analyst View",
        publication_date="Current application",
        source_type="Existing Databank capability",
    ),
    "Current application",
)

COMMERCIAL_HYPOTHESES = (
    CommercialHypothesis(
        "Integration & synergy realisation",
        "DKK 175m synergies realised in H1; 52 branches consolidated; employees reduced from 4,231 at YE2025 to 3,888 at H1 2026; Bankdata migration preparation is underway for 2027.",
        "The integration is moving beyond legal merger and structural consolidation into operating-model, process, people and technology harmonisation.",
        "Remaining synergy tracking; operating-model harmonisation; change/adoption; programme and dependency management; capacity prioritisation.",
        "Organisationsanalyse & Design; Transformation Tracker / change; IT Delivery Lead; capacity management.",
        "H1 2026 / 2027 target",
        (H1_2026_HIGHLIGHTS_SOURCE,),
        (
            "Where are the largest remaining integration dependencies?",
            "Which areas still operate with materially different legacy processes or models?",
            "Where is management most concerned about execution capacity?",
        ),
    ),
    CommercialHypothesis(
        "Customer & service model",
        "Management ambition to combine big-bank capabilities with local proximity; 88 Danish branches remain after 52 consolidations; positive private-customer development in housing and investment; Thursday bank-report and benchmark material identifies segmentation, proactive advice and adviser capacity as service-model themes.",
        "AL Sydbank must capture scale benefits while harmonising three legacy customer/service models without losing proximity and relationship continuity.",
        "Target customer / segment model; service tiers; adviser and specialist model; branch/channel role; data-driven proactive customer management; process simplification.",
        "Existing bank-report insight; Danske Bank benchmark; Process Excellence; service-model / operating-model work.",
        "H1 2026 / September 2026",
        (H1_2026_HIGHLIGHTS_SOURCE, THURSDAY_BENCHMARK_SOURCE, THURSDAY_ACCOUNT_SOURCE),
        (
            "Which customer segments should receive differentiated service models?",
            "What should the future role of branches, advisers and specialists be?",
            "How will the bank combine local ownership with more scalable servicing?",
        ),
    ),
    CommercialHypothesis(
        "Digital & platform enablement",
        "Bankdata transition is planned for 2027; management links the transition to lower complexity, improved customer-facing solutions and a scalable bank; Thursday benchmark work highlights architecture, AI operating models, data-driven customer activation and capacity routing as peer practices.",
        "The platform transition is both an execution risk and an opportunity to simplify processes, strengthen architecture governance and define future digital/data capabilities.",
        "Migration readiness and dependency transparency; architecture decision support; process simplification around the new platform; data/AI operating model; prioritised use cases with measurable business value.",
        "EA / architecture decision support; IT Delivery Lead; Process Excellence; AI adoption / operating model.",
        "2027 target / September 2026",
        (H1_2026_HIGHLIGHTS_SOURCE, THURSDAY_BENCHMARK_SOURCE),
        (
            "Which business capabilities are hardest to migrate or harmonise?",
            "Where are legacy dependencies most likely to constrain the target model?",
            "Which digital or AI capabilities should be designed into the future operating model rather than added afterwards?",
        ),
    ),
)

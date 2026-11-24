"""South Carolina facts, license data and copy. Facts checked Nov 24, 2026 against llr.sc.gov and PSI bulletins."""

CHECKED = "2026-11-24"
CHECKED_TEXT = "November 24, 2026"

SRC = {
    "clb": ("SC Contractor's Licensing Board, general information", "https://llr.sc.gov/clb/clb_general.aspx"),
    "clb_lic": ("SC Contractor's Licensing Board, licensure", "https://www.llr.sc.gov/clb/clb_licensure.aspx"),
    "clb_faq": ("SC Contractor's Licensing Board FAQ (group limits)", "https://llr.sc.gov/clb/faq.aspx"),
    "doc165": ("LLR Doc 165, GC and MC application requirements", "https://llr.sc.gov/clb/Forms/Doc165.pdf"),
    "abbr": ("CLB classification abbreviations and group limits", "https://www.llr.sc.gov/clb/PDFFiles/CLBClassificationAbbreviations.pdf"),
    "alarm": ("CLB burglar and fire alarm licensure", "https://llr.sc.gov/clb/licensure.aspx"),
    "rbc": ("SC Residential Builders Commission, Residential Builder", "https://llr.sc.gov/res/resbuilder.aspx"),
    "rbc_exam": ("SC Residential Builders Commission, examinations", "https://llr.sc.gov/res/exam.aspx"),
    "rbc_lic": ("SC Residential Builders Commission, licensure", "https://llr.sc.gov/res/licensure.aspx"),
    "psi_clb": ("PSI, South Carolina commercial contractor exams", "https://test-takers.psiexams.com/sccon"),
    "psi_rbc": ("PSI, South Carolina residential builder exams", "https://test-takers.psiexams.com/scrb"),
    "code": ("SC Code of Laws, Title 40 Chapter 11", "https://www.scstatehouse.gov/code/t40c011.php"),
    "alarm_act": ("SC Code of Laws, Title 40 Chapter 79 (Alarm System Business Act)", "https://scstatehouse.gov/code/t40c079.php"),
}

GC_GROUPS = [("Group 1", "$100,000"), ("Group 2", "$400,000"), ("Group 3", "$1,000,000"), ("Group 4", "$3,000,000"), ("Group 5", "Unlimited")]
MC_GROUPS = [("Group 1", "$35,000"), ("Group 2", "$100,000"), ("Group 3", "$200,000"), ("Group 4", "$400,000"), ("Group 5", "Unlimited")]

BOARDS = {
    "gc": "Contractor's Licensing Board (general contractor)",
    "mc": "Contractor's Licensing Board (mechanical contractor)",
    "alarm": "Contractor's Licensing Board (alarm business)",
    "rbc": "Residential Builders Commission",
    "local": "Local building department or county",
    "bl": "Business and Law exam (CLB or RBC)",
    "svc": "1 Exam Prep licensing services",
}

GROUPS = [
    ("commercial", "Commercial general contractor", "CLB general contractor classifications for regulated commercial work over $10,000.", "commercial"),
    ("mechanical", "Mechanical and alarm contractor", "CLB mechanical classifications plus the fire alarm business license.", "mechanical"),
    ("residential", "Residential Builders Commission", "Residential Builder and the three residential specialty licenses.", "residential"),
    ("local", "Electrician and plumber cards", "Journeyman and master credentials issued at the local level.", "local"),
    ("business", "Business and Law", "The business exam every CLB and RBC applicant has to pass.", "business"),
    ("services", "Licensing help", "Application service, business formation and starter courses.", "services"),
]

# slug: name, group, board, abbreviation, scope sentence, unique note, match keywords (lower-case, checked in order elsewhere)
L = [
    # --- CLB general ---
    ("commercial-general-building", "NASCLA Commercial General Building", "commercial", "gc", "BD / UB",
     "The NASCLA Commercial General Building exam is the path to an Unlimited Building (UB) license, which lets a South Carolina general contractor build commercial structures of any height.",
     "South Carolina accepts the NASCLA Accredited Examination for Commercial General Building in place of its own building exam, and a passing NASCLA score also waives the technical part of the Residential Builder exam if it is less than 3 years old."),
    ("limited-building", "Limited Building", "commercial", "gc", "BD / LB",
     "The Limited Building (LB) exam covers commercial building work up to 3 stories in height.",
     "LLR caps Limited Building licensees at Group 1, 2 or 3, so the largest job a Limited Building contractor can bid is $1,000,000. Contractors who need taller buildings or bigger jobs take the Unlimited Building (NASCLA) exam instead."),
    ("asphalt-paving", "Asphalt Paving", "commercial", "gc", "AP",
     "The Asphalt Paving classification covers commercial asphalt surfacing, base preparation and related grading for roads, lots and drives.",
     "Highway and paving candidates study plant mix, compaction, base courses and estimating, plus the SCDOT highway specifications that many paving jobs are bid against."),
    ("boiler-installation", "Boiler Installation", "commercial", "gc", "BL",
     "The Boiler Installation classification covers installing and repairing commercial boilers, piping and controls under the CLB.",
     "Boiler work in South Carolina also falls under the state boiler safety program, which the Contractor's Licensing Board oversees, so the exam leans heavily on the ASME codes and safe operating limits."),
    ("concrete", "Concrete", "commercial", "gc", "CT",
     "The Concrete classification covers commercial concrete foundations, slabs, structural concrete and formwork.",
     "Expect ACI design and construction questions, reinforcing steel placement, formwork pressure and curing, with the OSHA construction rules mixed in."),
    ("concrete-paving", "Concrete Paving", "commercial", "gc", "CP",
     "The Concrete Paving classification covers commercial concrete roads, parking areas, curbs and flatwork.",
     "Concrete paving candidates study slip-form and fixed-form paving, joints, finishing and the highway specifications used on public paving work."),
    ("grading", "Grading", "commercial", "gc", "GD",
     "The Grading classification covers commercial earthwork, excavation, site grading and erosion control.",
     "Grading questions focus on earthwork quantities, compaction, trench safety and the 811 utility locate rules that apply to every excavation in South Carolina."),
    ("marine", "Marine", "commercial", "gc", "MR",
     "The Marine classification covers docks, piers, bulkheads, seawalls and other work on or over the water.",
     "With more than 180 miles of coastline and the Intracoastal Waterway, marine work is a big part of South Carolina construction, and the exam covers pile driving, timber and concrete marine structures and waterfront safety."),
    ("nonstructural-renovation", "Nonstructural Renovation", "commercial", "gc", "NR",
     "The Nonstructural Renovation classification covers commercial interior renovation that does not touch structural elements: drywall, ceilings, flooring, millwork and finishes.",
     "Since January 1, 2025 the Nonstructural Renovation classification requires passing a PSI technical exam, so the books and courses here are built around that newer test."),
    ("pipelines", "Pipelines", "commercial", "gc", "PL",
     "The Pipelines classification covers commercial pipeline construction for gas, petroleum, water and other transmission lines.",
     "Pipeline candidates study trenching, pipe handling, welding and testing, plus the federal excavation safety rules."),
    ("roofing", "Roofing", "commercial", "gc", "RF",
     "The Roofing classification covers commercial roof systems, including low-slope membranes, metal panels, steep-slope roofing and flashing.",
     "The roofing exam pulls from the International Building Code, the NRCA roofing manuals and OSHA 29 CFR 1926, so knowing which book holds the answer matters as much as the trade knowledge."),
    ("structural-framing", "Structural Framing", "commercial", "gc", "SF",
     "The Structural Framing classification covers commercial framing in wood, light-gauge steel and structural steel.",
     "Framing candidates study load paths, connections, bracing and erection safety."),
    ("swimming-pools", "Swimming Pools", "commercial", "gc", "SP",
     "The Swimming Pools classification covers commercial and residential pool construction, equipment and repair.",
     "Pool contractors pass the PSI Swimming Pools exam and the Business Management and Law for Commercial Contractors exam, and there is no pre-approval needed to schedule them. South Carolina Regulation 61-51 for public pools is part of the study list."),
    ("water-sewer-lines", "Water and Sewer Lines", "commercial", "gc", "WL",
     "The Water and Sewer Lines classification covers underground water mains, sanitary sewers, storm drains and service lines.",
     "Line work questions cover pipe materials, bedding, testing, trench protection and the specifications water and sewer utilities use."),
    ("water-sewer-plants", "Water and Sewer Plants", "commercial", "gc", "WP",
     "The Water and Sewer Plants classification covers treatment plants, pump stations and lift stations.",
     "Plant candidates study process equipment, concrete tankage, piping and the safety rules for confined spaces."),
    ("wood-frame", "Wood Frame Structures", "commercial", "gc", "WF",
     "The Wood Frame Structures classification covers commercial wood-frame buildings.",
     "Expect code questions on wood design values, fasteners, sheathing and fire blocking, plus estimating and safety."),
    # --- CLB mechanical ---
    ("air-conditioning", "Air Conditioning", "mechanical", "mc", "AC",
     "The Air Conditioning classification covers commercial cooling systems, ductwork and controls.",
     "Air conditioning candidates work with the mechanical code, duct design and refrigerant handling, and the exam rewards fast lookups in tabbed code books."),
    ("heating", "Heating", "mechanical", "mc", "HT",
     "The Heating classification covers commercial heating systems, furnaces, hydronic systems and fuel gas piping.",
     "The heating exam leans on the mechanical and fuel gas codes plus heat loss and venting calculations."),
    ("refrigeration", "Refrigeration", "mechanical", "mc", "RG",
     "The Refrigeration classification covers commercial refrigeration equipment, walk-ins and process cooling.",
     "Refrigeration questions cover the refrigeration cycle, piping, charging, safety codes and EPA refrigerant rules."),
    ("plumbing", "Plumbing", "mechanical", "mc", "PB",
     "The Plumbing classification covers commercial plumbing, drainage, venting and water distribution.",
     "The commercial plumbing exam is built on the International Plumbing Code, and candidates who tab and highlight their code book finish with time to spare."),
    ("electrical", "Electrical", "mechanical", "mc", "EL",
     "The Electrical classification covers commercial electrical contracting under the CLB.",
     "Electrical contractor candidates face NEC code lookups and calculations; the NASCLA electrical exam is also accepted for some licenses, so check the bulletin before you buy books."),
    ("lightning-protection", "Lightning Protection", "mechanical", "mc", "LP",
     "The Lightning Protection classification covers air terminals, conductors and grounding for lightning protection systems.",
     "Lightning protection candidates study NFPA 780 and the UL standards for lightning protection installations."),
    ("fire-alarm", "Fire Alarm", "mechanical", "alarm", "FAC",
     "A Fire Alarm Contractor license lets a business design, install, service and maintain fire alarm systems in South Carolina.",
     "Under the Alarm System Business Act, the qualifying employee passes the PSI Fire Alarm exam and the Alarm Code of Laws exam, and the application needs an NTS Level I or II or a NICET Level II or III certificate, as applicable."),
    # --- RBC ---
    ("residential-builder", "Residential Builder", "residential", "rbc", "RBB",
     "A Residential Builder license from the Residential Builders Commission covers building and remodeling homes in South Carolina.",
     "The technical exam can be waived for a current SC General Contractor or for anyone who passed the NASCLA exam in the past 3 years, but the Business Management and Law exam still applies."),
    ("residential-electrical", "Residential Electrical", "residential", "rbc", "RBE",
     "A Residential Electrical license from the Residential Builders Commission covers electrical work on homes.",
     "South Carolina has exam waiver agreements for the residential electrical technical exam with North Carolina and Mississippi, and the NASCLA electrical exam is also accepted. The Business Management and Law exam is still required."),
    ("residential-hvac", "Residential HVAC", "residential", "rbc", "RBH",
     "A Residential HVAC license from the Residential Builders Commission covers heating, air conditioning and ventilation work on homes.",
     "Residential HVAC candidates pass the Residential HVAC exam and the Business Management and Law exam within 12 months of their Exam Eligibility letter."),
    ("residential-plumbing", "Residential Plumbing", "residential", "rbc", "RBP",
     "A Residential Plumbing license from the Residential Builders Commission covers plumbing work on homes.",
     "South Carolina has waiver agreements for the residential plumbing technical exam with North Carolina and Mississippi, but every applicant still passes the SC Business Management and Law exam."),
    # --- local ---
    ("journeyman-electrician", "Journeyman Electrician", "local", "local", "",
     "Journeyman electrician cards in South Carolina are issued by cities and counties, which usually require a PSI or ICC exam based on the National Electrical Code.",
     "Check with your local building department for the code edition and exam it uses. The study guides here come in 2023 NEC and 2026 NEC editions."),
    ("master-electrician", "Master Electrician", "local", "local", "",
     "Master electrician credentials in South Carolina are issued locally, and many electrical contractors also hold the CLB Electrical classification.",
     "Master-level exams lean on load calculations, service sizing and code lookups, so the calculations guide and a tabbed NEC are worth the most study time."),
    ("journeyman-plumber", "Journeyman Plumber", "local", "local", "",
     "Journeyman plumber cards in South Carolina are issued at the local level and tested on the International Plumbing Code.",
     "The study packages here are built on the 2021 International Plumbing Code with tabs and practice exams."),
    # --- business ---
    ("commercial-business-law", "Commercial Business and Law", "business", "bl", "",
     "The Business Management and Law for Commercial Contractors exam is required for every CLB general and mechanical license, and for alarm and pool licenses.",
     "The exam has 50 questions, a 125-minute limit and needs 35 correct answers to pass. It is open book, based on the NASCLA Contractor's Guide to Business, Law and Project Management, South Carolina edition."),
    ("residential-business-law", "Residential Business and Law", "business", "bl", "",
     "The Business Management and Law for Residential Builders exam is required for the Residential Builder, Residential Electrical, Residential HVAC and Residential Plumbing licenses.",
     "Candidates need a scale score of 68 to pass. The exam is open book and is based on the NASCLA Contractor's Guide for South Carolina Residential Builders."),
    # --- services ---
    ("licensing-services", "Licensing Help and Business Setup", "services", "svc", "",
     "Licensing help covers the paperwork around the exam: the LLR application, business formation, and starter courses that explain the process.",
     "The application service and LLC setup are done for you by the 1 Exam Prep team, and The 1 Package bundles exam prep with both."),
]

LICENSES = [dict(slug=s, name=n, group=g, board=b, abbr=a, scope=sc, note=no) for s, n, g, b, a, sc, no in L]
BY_SLUG = {l["slug"]: l for l in LICENSES}

# title matching rules, first match wins
RULES = [
    ("south dakota", None),
    ("introduction to becoming a south carolina limited building", "limited-building"),
    ("introduction to becoming a south carolina residential builder", "residential-builder"),
    ("introduction to becoming", "licensing-services"),
    ("application service", "licensing-services"), ("business formation", "licensing-services"),
    ("llc filing", "licensing-services"), ("license jumpstart", "licensing-services"),
    ("journeyman electrician", "journeyman-electrician"),
    ("nascla master electrical", "electrical"),
    ("master electrician", "master-electrician"),
    ("journeyman plumber", "journeyman-plumber"),
    ("contractors guide to business", "*bl"), ("contractor's guide to business", "*bl"),
    ("business management and law for commercial", "commercial-business-law"),
    ("commercial business and law", "commercial-business-law"),
    ("business management and law for residential", "residential-business-law"),
    ("residential business and law", "residential-business-law"),
    ("nascla residential electrician", "residential-electrical"),
    ("residential electrical", "residential-electrical"),
    ("residential hvac", "residential-hvac"),
    ("residential plumber", "residential-plumbing"),
    ("residential builder", "residential-builder"),
    ("air conditioning", "air-conditioning"),
    ("heating contractor", "heating"),
    ("refrigeration", "refrigeration"),
    ("commercial plumb", "plumbing"),
    ("commercial electrician", "electrical"),
    ("lightning protection", "lightning-protection"),
    ("fire alarm", "fire-alarm"),
    ("nascla commercial general building", "commercial-general-building"),
    ("limited building", "limited-building"),
    ("asphalt paving", "asphalt-paving"),
    ("boiler", "boiler-installation"),
    ("concrete paving", "concrete-paving"),
    ("concrete", "concrete"),
    ("grading", "grading"), ("811 excavator", "grading"), ("highway construction", "asphalt-paving"),
    ("marine", "marine"),
    ("non-structural renovation", "nonstructural-renovation"), ("non structural renovation", "nonstructural-renovation"),
    ("pipelines", "pipelines"),
    ("roofing", "roofing"),
    ("structural framing", "structural-framing"),
    ("swimming pool", "swimming-pools"),
    ("water & sewer plant", "water-sewer-plants"), ("water and sewer plant", "water-sewer-plants"),
    ("water & sewer lines", "water-sewer-lines"), ("water and sewer lines", "water-sewer-lines"),
    ("wood frame", "wood-frame"),
]


def classify(title):
    t = title.lower()
    for k, v in RULES:
        if k in t:
            if v == "*bl":
                return "residential-business-law" if "residential" in t else "commercial-business-law"
            return v
    return "unmatched"


# package type: (key, label, rank) first match wins; rank sets sort order (lower = shown first)
TYPES = [
    ("the 1 package", "The 1 Package", 1),
    ("ultimate exam prep rental", "Ultimate rental package", 2),
    ("instructor led", "Study package with NEC course", 2),
    ("ultimate combo", "Ultimate combo", 3),
    ("ultimate exam prep package", "Ultimate prep package", 3),
    ("complete pass package", "Complete pass package", 3),
    ("ultimate package", "Ultimate service package", 3),
    ("jumpstart", "Jumpstart package", 3),
    ("rental", "Books and courses rental", 4),
    ("flash cards & national electrical code + tabs", "Super combo", 4),
    ("calculations study guides & national electrical code", "Study guide, calculations and NEC", 5),
    ("highlighted", "Highlighted and tabbed books", 5),
    ("live virtual", "Live virtual training", 6),
    ("code combo with tabs", "Study guide and NEC with tabs", 6),
    ("complete book", "Complete book package", 7), ("book package", "Complete book package", 7), ("book set", "Complete book package", 7),
    ("exam prep package", "Exam prep package", 7),
    ("online exam prep", "Online course", 8), ("online practice", "Online practice questions", 9),
    ("flash card combo", "Study guide and flash cards", 9),
    ("introduction to", "Starter course", 9),
    ("pre-printed tabs", "Pre-printed tabs", 10),
    ("exam prep and study guide", "Study guide", 10),
    ("service", "Service", 5), ("formation", "Service", 5),
    ("contractors guide", "Business and Law book", 8), ("contractor's guide", "Business and Law book", 8),
]


def ptype(title):
    t = title.lower()
    for k, lab, r in TYPES:
        if k in t:
            return lab, r
    return "Book", 9


ONLINE_TYPES = {"Online course", "Online practice questions", "Live virtual training", "Service", "Starter course", "Ultimate service package"}

STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "DBPR"]

"""Blog posts for passyoursouthcarolinacontractorexam.com. Facts checked Nov 24, 2026 against LLR, PSI and the SC Code."""

AUTHOR = "Max Ace"

BSRC = {
    "clb": ("SC Contractor's Licensing Board, general information", "https://llr.sc.gov/clb/clb_general.aspx"),
    "clb_lic": ("SC Contractor's Licensing Board, licensure", "https://www.llr.sc.gov/clb/clb_licensure.aspx"),
    "clb_faq": ("SC Contractor's Licensing Board FAQ (group limits)", "https://llr.sc.gov/clb/faq.aspx"),
    "waiver": ("CLB waiver and reciprocity agreements", "https://llr.sc.gov/clb/PDFFILES/WAIVER%20AGREEMENTS.pdf"),
    "rbc": ("SC Residential Builders Commission, Residential Builder", "https://llr.sc.gov/res/resbuilder.aspx"),
    "rbc_exam": ("SC Residential Builders Commission, examinations", "https://llr.sc.gov/res/exam.aspx"),
    "rbc_lic": ("SC Residential Builders Commission, licensure and waivers", "https://llr.sc.gov/res/licensure.aspx"),
    "rbc_spec": ("SC Residential Builders Commission, specialty contractor registration", "https://llr.sc.gov/res/resspecialty.aspx"),
    "code59": ("SC Code of Laws, Title 40 Chapter 59 (residential builders)", "https://www.scstatehouse.gov/code/t40c059.php"),
    "code11": ("SC Code of Laws, Title 40 Chapter 11 (contractors)", "https://www.scstatehouse.gov/code/t40c011.php"),
    "psi_clb": ("PSI, South Carolina commercial contractor exams", "https://test-takers.psiexams.com/sccon"),
    "psi_rbc": ("PSI, South Carolina residential builder exams", "https://test-takers.psiexams.com/scrb"),
}

POSTS = [dict(
    slug="south-carolina-contractor-license-questions-answered",
    title="South Carolina Contractor License: 15 Questions Answered",
    meta_title="SC Contractor License: 15 Questions Answered (2026)",
    meta_desc="Straight answers to the 15 most-asked South Carolina contractor license questions: CLB vs RBC, the $10,000 rule, exams, costs, job limits and reciprocity.",
    date="2026-11-24", updated="2026-11-24",
    excerpt="CLB or Residential Builders Commission, the $10,000 rule, open-book PSI exams, fees, job limits, reciprocity and the homeowner exemption, answered in plain English.",
    tags=["Licensing", "Exams", "South Carolina"],
    lead=("Most South Carolina contractors need a license from one of two LLR boards. The Contractor's Licensing Board covers regulated commercial work over $10,000, "
          "and the Residential Builders Commission covers homes. Both require a PSI trade exam and an open-book Business and Law exam. "
          "Here are straight answers to the 15 questions people search most."),
    takeaways=["CLB license needed for regulated commercial work over $10,000.", "Residential Builder license needed for home building and remodeling jobs over $5,000.",
               "Commercial Business and Law: 50 questions, 125 minutes, 35 to pass, open book.", "CLB licensure fee: $350; job limits run from $100,000 (Group 1) to unlimited.",
               "Most candidates study 4 to 8 weeks."],
    sections=[
        ("do-you-need-a-license", "Do you need a contractor license in South Carolina?",
         "<p>Yes, once a job crosses the state's dollar thresholds. A Contractor's Licensing Board (CLB) license is required for anyone performing regulated commercial construction over $10,000. "
         "That threshold rose from $5,000 on May 19, 2023, when Act 69 took effect. Residential work runs through the Residential Builders Commission (RBC), which requires a license or registration "
         "to engage in residential building or specialty contracting. Individual electricians and plumbers also need a card from the city or county where they work. "
         "Pick the board by the kind of work and its value, then pick the classification.</p>"),
        ("work-without-a-license", "How much work can you do without a license in South Carolina?",
         "<p>The limits depend on the board. On commercial jobs, regulated work of $10,000 or less does not need a CLB license, although local permits still apply. "
         "On homes, a Residential Specialty Contractor registration is needed once a single job goes over $500, and a Residential Builder license is needed once the total goes over $5,000. "
         "The $500 figure replaced the old $200 limit in 2022, so older guides that quote $200 are out of date. "
         "If a job is close to a limit, ask LLR before you bid.</p>"),
        ("clb-vs-rbc", "What is the difference between the CLB and the Residential Builders Commission?",
         "<p>The two boards are separate agencies inside the Department of Labor, Licensing and Regulation, with their own exams, fees and forms.</p>"
         "<table><thead><tr><th></th><th>Contractor's Licensing Board</th><th>Residential Builders Commission</th></tr></thead><tbody>"
         "<tr><td>Work covered</td><td>Commercial general and mechanical, alarm, boiler</td><td>Homes: builders and residential specialty trades</td></tr>"
         "<tr><td>Trigger</td><td>Regulated work over $10,000</td><td>Builder over $5,000; specialty over $500</td></tr>"
         "<tr><td>Exams</td><td>PSI trade exam plus Commercial Business and Law</td><td>PSI trade exam plus Residential Business and Law</td></tr>"
         "<tr><td>Order of steps</td><td>Pass exams, then apply</td><td>Apply, get Exam Eligibility letter, then test</td></tr>"
         "<tr><td>Job limits</td><td>Group 1 to Group 5</td><td>No dollar cap on residential work</td></tr></tbody></table>"
         "<p>A CLB license also lets the entity do residential work. An RBC license never covers commercial work.</p>"),
        ("how-to-get-gc-license", "How do you get a general contractor license in South Carolina?",
         "<ol><li>Choose your classification, such as Building, Roofing or Concrete, from the CLB list.</li>"
         "<li>Name a qualifying party who will take the exams for the business.</li>"
         "<li>Pass the PSI technical exam for each classification and the Business Management and Law for Commercial Contractors exam. No pre-approval is needed to book.</li>"
         "<li>Prepare a financial statement or surety bond, which sets your license group.</li>"
         "<li>Send LLR the application (Doc. 165), your PSI pass sheets and the $350 fee.</li></ol>"
         "<p>Building candidates choose between the Limited Building exam (up to 3 stories) and the NASCLA Commercial General Building exam for unlimited height. "
         "See the <a href='/how-to-get-licensed/'>full licensing guide</a> for each step in detail.</p>"),
        ("how-much-does-it-cost", "How much does a South Carolina contractor license cost?",
         "<p>The CLB licensure fee is $350 for a general or mechanical contractor license. On top of that you pay PSI directly for each exam, plus the cost of your financial statement or bond. "
         "Groups 1 and 2 can use an owner-prepared financial statement or a surety bond, which keeps the cost low for smaller contractors. "
         "Study materials are the other big cost. On this site, South Carolina prep runs from $14.95 for a single regulation book to $4,964 for an all-inclusive package with application help. "
         "Most trade online courses cost $295, and pre-printed tabs start under $50. Browse the <a href='/licenses/'>license pages</a> for exact prices by trade.</p>"),
        ("is-the-exam-open-book", "Is the South Carolina contractor exam open book?",
         "<p>Yes. PSI gives the CLB and RBC trade exams and both Business and Law exams as open-book tests, using the references on each candidate bulletin. "
         "Open book does not mean easy. The clock is the real opponent: on the commercial Business and Law exam you get about 2.5 minutes per question. "
         "Candidates who have tabbed and highlighted their books ahead of time find answers in seconds instead of minutes. "
         "Bring the exact editions listed in the bulletin, because an older or newer edition can put the answer on a different page or change it entirely.</p>"),
        ("business-and-law-questions", "How many questions are on the South Carolina Business and Law exam?",
         "<p>The Business Management and Law for Commercial Contractors exam has 50 questions and a 125-minute time limit. You need 35 correct answers, or 70 percent, to pass. "
         "The exam is based on the NASCLA Contractor's Guide to Business, Law and Project Management, South Carolina edition, and covers estimating, contracts, lien law, taxes, payroll and safety. "
         "The residential version, Business Management and Law for Residential Builders, needs a scale score of 68. "
         "Both are required: the commercial version for every CLB license and the residential version for every RBC license. "
         "The <a href='/commercial-business-law/'>commercial Business and Law page</a> lists the books and courses for it.</p>"),
        ("how-hard-is-it", "How hard is the South Carolina contractor exam?",
         "<p>Hard enough that preparation matters more than experience. Field experience helps with the trade questions, but many questions test where a rule lives in a code or reference book. "
         "Candidates who fail usually run out of time rather than knowledge. Four habits make the biggest difference:</p>"
         "<ul><li>Use the exact book editions on the PSI bulletin.</li><li>Tab every chapter and the most-used tables before exam day.</li>"
         "<li>Answer easy questions first and flag the slow ones.</li><li>Take at least 2 full timed practice exams in the final week.</li></ul>"),
        ("how-long-does-it-take", "How long does it take to get a contractor license in South Carolina?",
         "<p>Plan on 2 to 4 months from start to license. Most candidates study for 4 to 8 weeks, and many take the trade exam and Business and Law in the same week. "
         "CLB candidates can book a PSI seat as soon as they are ready, then apply after passing. LLR's review time depends on how complete the application is. "
         "RBC candidates add a step at the front: they apply first and wait for the Exam Eligibility letter, which is valid for 1 year. "
         "Missing financial documents and unsigned experience forms are the most common causes of delay.</p>"),
        ("license-groups", "What are the license groups and job limits?",
         "<p>Every CLB license carries a group number from 1 to 5 that caps the value of any single job or bid. The group comes from your working capital and net worth, or from a surety bond.</p>"
         "<table><thead><tr><th>Group</th><th>General contractor limit</th><th>Mechanical contractor limit</th></tr></thead><tbody>"
         "<tr><td>1</td><td>$100,000</td><td>$35,000</td></tr><tr><td>2</td><td>$400,000</td><td>$100,000</td></tr>"
         "<tr><td>3</td><td>$1,000,000</td><td>$200,000</td></tr><tr><td>4</td><td>$3,000,000</td><td>$400,000</td></tr>"
         "<tr><td>5</td><td>Unlimited</td><td>Unlimited</td></tr></tbody></table>"
         "<p>The license shows the classification code followed by the group, so BD3 means Building work up to $1,000,000 per job.</p>"),
        ("reciprocity", "Does South Carolina have reciprocity with other states?",
         "<p>Partly. South Carolina has exam waiver agreements, not full reciprocity. The CLB accepts certain technical exams passed in some states, but every waiver applicant still passes the South Carolina Business Management and Law exam. "
         "For the Residential Builder license, the RBC has technical exam waivers with Alabama, Georgia, Louisiana, Mississippi and North Carolina, and it accepts the NASCLA exam. "
         "Residential electrical waivers exist with North Carolina and Mississippi, as do residential plumbing waivers. "
         "Your home-state license must be current and in good standing, and a license that was grandfathered in does not qualify.</p>"),
        ("homeowner-exemption", "Can a homeowner build their own house without a license in South Carolina?",
         "<p>Yes, under the owner-builder exemption in Section 40-59-260 of the SC Code. As the owner, you may act as your own builder on a one-family or two-family home without a license. "
         "You must supervise the construction yourself, and the home must be for your own use and occupancy. "
         "The exemption does not apply to a house built for sale or rent. Counties ask owner-builders to sign a disclosure statement when they pull the permit, "
         "so check with your local building department before work starts.</p>"),
        ("handyman", "Do handymen need a license in South Carolina?",
         "<p>South Carolina has no handyman license, but residential work is regulated by job value. A Residential Specialty Contractor registration is needed for residential jobs over $500. "
         "Registration requires no exam, and one registration covers up to 3 trade classifications, such as painting, drywall or flooring. "
         "Contractors who need more than 3 classifications at a time must become a licensed Residential Builder. "
         "Electrical, plumbing and HVAC work on homes needs a residential specialty license by exam, not a simple registration.</p>"),
        ("residential-builder", "How do you get a residential builder license in South Carolina?",
         "<p>Apply to the Residential Builders Commission first, with proof of at least 1 year of residential building experience. "
         "The experience can come from any state or country. Once the Commission approves the application, it sends an Exam Eligibility letter. "
         "You then schedule two PSI exams, the Residential Builder exam and Business Management and Law for Residential Builders, and must pass both within the year. "
         "A current SC General Contractor or anyone who passed the NASCLA exam in the past 3 years can skip the trade exam. "
         "The <a href='/residential-builder/'>Residential Builder page</a> lists every book and course for the exam.</p>"),
        ("expiration", "When do South Carolina contractor licenses expire?",
         "<p>CLB licenses run on a 2-year cycle that depends on the license type. All general contractor licenses expire on October 31 of even-numbered years, and all mechanical contractor licenses expire on October 31 of odd-numbered years. "
         "Burglar and fire alarm licenses follow their own schedule; the 2026 to 2028 renewal deadline was October 29, 2026. "
         "A license not renewed by the deadline lapses, and working on a lapsed license counts as unlicensed work. "
         "Residential Builders Commission licenses renew on the schedule shown on the RBC renewal page, so check your license card for the date.</p>"),
    ],
    faq=[
        ("What is the dollar limit for needing a CLB license?", "Regulated commercial work over $10,000 needs a CLB general or mechanical contractor license. The limit was $5,000 until May 19, 2023."),
        ("Do I need approval before booking the CLB exam?", "No. CLB candidates book directly with PSI and apply after passing. RBC candidates must apply first and wait for the Exam Eligibility letter."),
        ("What score passes the commercial Business and Law exam?", "35 correct answers out of 50, which is 70 percent, within 125 minutes."),
        ("How much experience do I need for a Residential Builder license?", "At least 1 year of residential building experience, which can come from any state or country."),
        ("Can I use the NASCLA exam in South Carolina?", "Yes. NASCLA is accepted for the Unlimited Building classification, and a pass within 3 years waives the Residential Builder trade exam."),
        ("Where can I buy the exam books?", "Every South Carolina license page on this site lists the books, tabs and courses for that exam, with free USPS Media Mail shipping on books."),
    ],
    sources=["clb", "clb_lic", "clb_faq", "waiver", "rbc", "rbc_exam", "rbc_lic", "rbc_spec", "code59", "code11", "psi_clb", "psi_rbc"],
)]

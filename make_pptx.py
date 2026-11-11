import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_presentation():
    prs = Presentation()
    # Set 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Blank slide layout
    blank_layout = prs.slide_layouts[6]

    slides_data = [
        {
            "img": "presentation/slide1_about.png",
            "title": "Diagram Design: AI-Powered Diagram Generation",
            "notes": (
                "Slide 1: About the Project\n\n"
                "• Developer: Cathryn Lavery (founder of LittleMight).\n"
                "• Project: Diagram Design is an open-source Agent Skill that enables AI coding agents "
                "to generate publication-grade technical diagrams as self-contained HTML + SVG files.\n"
                "• Core Problem: Manual drag-and-drop diagramming tools (Figma, draw.io) demand high effort and "
                "break developer focus, while default code-to-diagram generators (e.g. raw Mermaid) often yield "
                "generic, unbranded, cluttered layouts.\n"
                "• Key Architectural Distinction: Diagram Design is an agent skill, not a standalone graphical "
                "editor or a trained AI model. It supplies layout rules, 4px grid constraints, and editorial taste "
                "to general-purpose AI coding agents."
            )
        },
        {
            "img": "presentation/slide2_how_it_works.png",
            "title": "How It Works",
            "notes": (
                "Slide 2: How It Works & Key Capabilities\n\n"
                "• 4-Stage Operational Pipeline:\n"
                "  1. Describe: User prompts the agent with natural language.\n"
                "  2. Select & Plan: Agent chooses from 45 diagram types and applies 4px grid constraints.\n"
                "  3. Generate: Agent writes clean, self-contained semantic HTML with inline SVG.\n"
                "  4. Render & View: User opens the .html file directly in any modern browser.\n"
                "• Key Capabilities:\n"
                "  - 45 standardized diagram types.\n"
                "  - Conversational natural-language creation and iterative refinement.\n"
                "  - Disciplined visual hierarchy: 1px hairlines, 1 focal accent color, zero drop shadows.\n"
                "  - Brand customization via 60-second URL onboarding with WCAG AA contrast verification.\n"
                "  - Native import and editorial redesign of draw.io, Mermaid, and Excalidraw files.\n"
                "  - Self-contained HTML output with zero runtime dependencies."
            )
        },
        {
            "img": "presentation/slide3_advantages.png",
            "title": "Advantages of Diagram Design",
            "notes": (
                "Slide 3: Advantages of Diagram Design\n\n"
                "Six Core Architectural and Practical Benefits:\n"
                "1. Reduced manual drawing and formatting effort.\n"
                "2. Consistent design and visual hierarchy on a strict 4px grid.\n"
                "3. Easier diagram creation through natural-language prompts.\n"
                "4. Support for diverse diagram types and technical scenarios.\n"
                "5. Portable HTML/SVG output viewable immediately in any browser.\n"
                "6. Cross-agent compatibility across Cursor, Claude Code, Codex, GitHub Copilot, Qoder, and Factory Droid.\n\n"
                "Key Takeaway: Diagram Design helps developers communicate complex systems more clearly while reducing the effort required to create and style diagrams."
            )
        },
        {
            "img": "presentation/slide4_use_cases.png",
            "title": "Where Can Diagram Design Be Used?",
            "notes": (
                "Slide 4: Use Cases and Application Areas\n\n"
                "Central Hub Architecture connecting 6 Core Technical Domains:\n"
                "1. Software Development: Application architecture, API interactions, sequence diagrams, and DB schemas.\n"
                "2. Education: Algorithms, core computer science concepts, and interactive lecture diagrams.\n"
                "3. Data Engineering: Multi-tier Medallion pipelines (Bronze/Silver/Gold), ETL flows, and data models.\n"
                "4. Business Analysis: Business process flows, decision flowcharts, and customer journeys.\n"
                "5. Project Management: Strategic timelines, task dependency graphs, Gantt schedules, and story maps.\n"
                "6. Technical Documentation: README architecture overviews, developer guides, and Architecture Decision Records (ADRs).\n\n"
                "Practical Walkthrough Example: A developer describes a web application’s frontend, backend, database, and cache. The AI agent uses Diagram Design to create a structured architecture diagram."
            )
        },
        {
            "img": "presentation/slide5_future_conclusion.png",
            "title": "Future Scope and Conclusion",
            "notes": (
                "Slide 5: Future Scope and Conclusion\n\n"
                "Clear Distinction between Current Production Features and Proposed Future Additions:\n"
                "• Current Capabilities: 45 diagram types, URL brand onboarding, multi-agent host compatibility, draw.io/Mermaid/Excalidraw imports, self-contained HTML/SVG.\n"
                "• Proposed Future Roadmap:\n"
                "  1. Interactive drag-and-drop editing for post-generation canvas adjustments.\n"
                "  2. Real-time collaborative editing and shared review threads.\n"
                "  3. Convenient 1-click export to native PPTX, PDF, and high-res vector formats.\n"
                "  4. Diagram version history and Git-integrated visual diff tracking.\n"
                "  5. Enhanced automated validation for disconnected elements and overlapping boxes.\n"
                "  6. Expanded ecosystem integration with additional IDEs and CI/CD doc bots.\n\n"
                "Conclusion: Diagram Design demonstrates how AI agent skills can turn natural-language instructions into structured, visually consistent diagrams. Its approach can benefit software development, education, data engineering, business analysis, and technical documentation.\n\n"
                "Official Repository: https://github.com/cathrynlavery/diagram-design"
            )
        }
    ]

    for item in slides_data:
        slide = prs.slides.add_slide(blank_layout)
        
        # Add the 16:9 full slide background visual
        slide.shapes.add_picture(
            item["img"],
            left=Inches(0),
            top=Inches(0),
            width=Inches(13.333),
            height=Inches(7.5)
        )
        
        # Add slide notes for speaker/presenter view
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = item["notes"]

    output_pptx = "presentation/diagram_design_presentation.pptx"
    prs.save(output_pptx)
    print(f"Successfully generated PowerPoint presentation: {output_pptx}")

if __name__ == "__main__":
    create_presentation()

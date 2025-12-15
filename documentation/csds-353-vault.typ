#import "common/lib/contentBox.typ": contentBox
#import "common/lib/slideLayouts.typ": theme, mainTitle, layoutA, layoutATwoCols, layoutATwoColsWithTitle, layoutBTwoCols, layoutC, layoutCTwoColsWithTitle, layoutDTwoCols

#mainTitle(
  title: "CSDS-353 Vault",
  subtitle: "Oscar Muñoz <oscar.munoz@jala.university>",
  content: [

    #v(160pt)

    #contentBox(
      fill: luma(150, 30%),
      text(
        fill: white,
        size: 20pt,
        [
          This is a complementary document containing notes and references for the *Deep Learning & Generative AI* course.
        ],
      ),
    )
  ],
)

#layoutC(
  title: "Agenda",
  content: [
    #v(20pt)
    #text(
      size: 28pt,
      [
        1. Introduction and Context
        2. Identified Problem
        3. Project Goals and Scope
        4. Proposed Solution
        5. System Architecture
        6. How the Assistant Works
        7. Technologies
        8. Demo
        9. Challenges and Lessons Learned
        10. Benefits, Conclusions, and Next Steps
      ]
    )
  ]
)

#layoutC(
  title: "Introduction and Context",
  content: [

    #v(50pt)
    == Did you know?

    #contentBox(
      fill: theme.primaryLightest,
      text(
        fill: white,
        size: 28pt,
        [
          The Central Bank of Colombia reported that by the end of 2024, cash is still the most used payment method for daily purchases, with 77.8%.
        ],
      ),
    )
    #text(size: 15pt, fill: black, "https://www.larepublica.co/finanzas/casi-80-de-las-transacciones-que-se-hacen-en-colombia-aun-se-realizan-en-efectivo-4042298")
  ]
)

#layoutC(
  title: "Identified Problem",
  content: [
    #align(center + horizon,
    [
      #text(
        size: 30pt,
        weight: "bold",
        fill: theme.primary,
        [
          If there are digital wallets, mobile banks, and electronic payments, why do most people still prefer cash?
        ],
      )
    ])
  ]
)

#layoutA(
  content: [
    #align(horizon,
    [
      #text(
        size: 28pt,
        [
          One main reason is the lack of access to technology and low digital skills in some parts of the population. Poor internet connection in rural areas and low financial education make it hard for many people to use digital services.

          #v(30pt)
          Also, many people do not trust digital systems and are afraid of fraud.
        ]
      )
    ])
  ]
)

#layoutA(
  content: [
    #align(center + horizon,
    [
      #image("images/capstone/survey_example.png", width: 85%)
    ])
    #text(size: 15pt, fill: black, "https://www.larepublica.co/finanzas/casi-80-de-las-transacciones-que-se-hacen-en-colombia-aun-se-realizan-en-efectivo-4042298")
  ]
)

#layoutC(
  title: "Project Goals and Scope",
  content: [
    #align(horizon, [
      #text(
        size: 26pt,
        [
          - Build a generative assistant using the Model Context Protocol (MCP)
          - Use pre-trained models and apply fine-tuning when needed
          - Design clear prompts to control and guide model behavior
          - Combine text understanding with object detection
          - Focus on a real and practical financial use case
        ]
      )
    ])
  ]
)

#layoutC(
  title: "Proposed Solution",
  content: [
    #align(center + horizon,
    [
      #image("images/capstone/logo.png", width: 70%)
    ])
  ]
)

#layoutA(
  content: [
    #align(horizon,
    [
      #text(size: 28pt)[
        *Finai* is an assistant where users can ask simple questions about finance. It uses information from sources like the Financial Superintendence of Colombia, the National Savings Fund, and blogs from major Colombian banks.

        #v(50pt)

        While users learn how to manage their money and use digital tools, Finai also offers a powerful feature: *Colombian banknote detection*.
      ]
    ])
  ]
)

#layoutA(
  content: [
    #align(horizon,
    [
      #grid(
        columns: (1fr, 1fr),
        [
          #align(center)[#image("images/capstone/banks_logos.png", width: 90%)]
        ],
        [
          #align(center)[#image("images/capstone/fna_logo.png", width: 50%)]
          #align(center)[#image("images/capstone/sfc_logo.png", width: 50%)]
        ],
      )
    ])
  ]
)

#layoutC(
  title: "System Architecture",
  content: [
    #align(center + horizon,
    [
      #image("images/capstone/architecture.png", width: 110%)
    ])
  ]
)

#layoutC(
  title: "Technologies",
  content: [
    #align(horizon,
    [
      #grid(
        columns: (1fr,1fr,1fr),
        [
          #align(center)[#image("images/capstone/google_embedings_logo.png", width: 80%)],
          #align(center)[#image("images/capstone/langchain_logo.png", width: 80%)]
          #align(center)[#image("images/capstone/fastapi_logo.png", width: 80%)]
        ],
        [
          #align(center)[#image("images/capstone/chroma_logo.png", width: 30%)]
          #align(center)[#image("images/capstone/streamlit_logo.png", width: 70%)]
          #align(center)[#image("images/capstone/claude_logo.png", width:50%)]
        ],
        [
          #align(center)[#image("images/capstone/colab_logo.png", width: 30%)]
          #align(center)[#image("images/capstone/roboflow_logo.png", width: 60%)]
          #align(center)[#image("images/capstone/yolo_logo.png", width: 70%)]

        ],
      )
    ])
  ]
)

#layoutC(
  title: "How the Assistant Works – Chat",
  content: [
    #align(center + horizon,
    [
      #image("images/capstone/chat_architecture.png", width: 75%)
    ])
  ]
)

#layoutC(
  title: "How the Assistant Works – Object Detection",
  content: [
    #align(center + horizon,
    [
      #image("images/capstone/yolo_architecture.png", width: 100%)
    ])
  ]
)

#layoutA(
  content: [
    #align(center + horizon, [
      #text(
        size: 50pt,
        weight: "bold",
        fill: theme.primary,
        [
          Demo
        ],
      )
      #v(10pt)
      #link(
        "https://deeplearning-oscar-munoz.streamlit.app/",
        text(
          size: 15pt,
          fill: black,
          [
            https://deeplearning-oscar-munoz.streamlit.app/
          ]
        )
      )
    ])
  ]
)

#layoutC(
  title: "Challenges and Lessons Learned",
  content: [
    #align(horizon, [
      #text(
        size: 26pt,
        [
          - First time working with the Model Context Protocol (MCP)
          - Limited documentation and real examples
          - Integrating MCP with a REST API
          - Iterating on prompts to improve model answers
          - Learning how and when to apply fine-tuning
        ]
      )
    ])
  ]
)


#layoutC(
  title: "Benefits, Conclusions, and Next Steps",
  content: [
    #align(horizon, [
      #contentBox(
        fill: theme.primaryLightest,
        text(
          size: 25pt,
          fill: white,
          [
            With Finai, anyone with a smartphone can learn basic finance concepts in a simple way.

            #v(15pt)

            Its banknote detection feature could be used in the future to teach children about money and could also help people with visual impairments by using text-to-speech.
          ]
        )
      )
    ])
  ]
)

#layoutA(
  content: [
    #align(center + horizon, [
      #text(
        size: 40pt,
        weight: "bold",
        fill: theme.primary,
        [
          “An investment in knowledge pays the best interest.”
        ],
      )

      #text([(Benjamin Franklin)])
    ])
  ]
)

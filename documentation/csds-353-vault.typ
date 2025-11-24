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
          Este es un documento complementario que contiene notas y referencias para el curso *Deep Learning & Generative AI*.
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
        1. Introducción
        2. Problema Identificado
        3. Solución Propuesta
        4. ¿Como funciona?
        5. Tecnologías
        6. Demo
        7. Beneficios y Conclusiones
      ]
    )
  ]
)

#layoutC(
  title: "Introducción",
  content: [

    #v(50pt)
    == ¿Sabías que?

    #contentBox(
      fill: theme.primaryLightest,
      text(
        fill: white,
        size: 28pt,
        [
          El Banco de la República reveló que para finales del 2024 el efectivo continúa liderando como el instrumento de pago más utilizado en los consumos diarios con el 77,8%,
        ],
      ),
    )
    #text(size: 15pt,fill: black,"https://www.larepublica.co/finanzas/casi-80-de-las-transacciones-que-se-hacen-en-colombia-aun-se-realizan-en-efectivo-4042298")
  ]
)

#layoutC(
  title: "Problema Identificado",
  content: [
    #align(center + horizon,
    [
      #text(
        size: 30pt,
        weight: "bold",
        fill: theme.primary,
        [
          Si hoy existen tantas billeteras digitales, bancos 100% móviles, medios de pago electrónicos, etc... ¿por qué la mayoría de las personas siguen prefiriendo el efectivo?
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
          Uno de los principales motivos se debe a la falta de acceso y familiaridad tecnológica en algunos sectores de la población. Los problemas de conectividad en zonas rurales y la baja educación financiera impiden que muchos ciudadanos adopten estas alternativas con mayor frecuencia.

          #v(30pt)
          Además, la desconfianza hacia los sistemas digitales y el temor a fraudes siguen siendo preocupaciones comunes entre las personas.
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
    #text(size: 15pt,fill: black,"https://www.larepublica.co/finanzas/casi-80-de-las-transacciones-que-se-hacen-en-colombia-aun-se-realizan-en-efectivo-4042298")
  ]
)

#layoutC(
  title: "Solución Propuesta",
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
        *Finai* es un asistente al que puedes preguntarle, de forma sencilla dudas comunes del mundo financiero con información de fuentes como la superintendencia financiera, fondo nacional del ahorro y blogs de los principales bancos de colombia.

        #v(50pt)

        Además, mientras aprendes a manejar mejor tus finanzas y a moverte en el mundo digital, Finai te ofrece una función poderosa, *"la detección de billetes colombianos"*.
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
  title: "Tecnologías",
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
          #align(center)[#image("images/capstone/gemini_logo.png", width:75%)]
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
  title: "¿Como funciona? - Chat",
  content: [
    #align(center + horizon,
    [
      #image("images/capstone/chat_architecture.png", width: 75%)
    ])
  ]
)

#layoutC(
  title: "¿Como funciona? - Detección",
  content: [
    #align(center + horizon,
    [
      #image("images/capstone/yolo_architecture.png", width: 100%)
    ])
  ]
)

#layoutA(
  content: [
    #align(center + horizon,
    [
      #text(
        size: 50pt,
        weight: "bold",
        fill: theme.primary,
        [
          Demo
        ],
      )
    ])
  ]
)

#layoutC(
  title: "Beneficios y Conclusiones",
  content: [
    #align(horizon, [
      #contentBox(
        fill: theme.primaryLightest,
        text(
          size: 25pt,
          fill: white,
          [
            Con Finai cualquier persona con un teléfono puede aprender conceptos básicos de finanzas de forma sencilla y accesible.

            #v(15pt)

            Además, su tecnología de identificación de billetes la puede convertir a futuro en una herramienta útil para enseñar a los niños las diferentes denominaciones, y puede integrarse con sistemas de text-to-speech para ayudar a personas con baja visión a reconocer billetes mediante audio.
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
          “Invertir en conocimiento paga el mejor interés”
        ],
      )

      #text([(Benjamín Franklin)])
    ])
  ]
)

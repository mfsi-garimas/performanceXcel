import {
  Document,
  Packer,
  Paragraph,
  TextRun,
  AlignmentType,
  BorderStyle,
  ImageRun,
} from "docx";

import { saveAs } from "file-saver";
import getFileName from "./GenerateRandomFileName";

import logo from "/performanceXcel-logo.png";

type Props = {
  evaluationData: any;
};

const DownloadDocButton = ({
  evaluationData,
}: Props) => {
  const createHeading = (
    text: string,
    size = 32
  ) =>
    new Paragraph({
      children: [
        new TextRun({
          text,
          bold: true,
          size,
          color: "000000",
        }),
      ],

      spacing: {
        after: 200,
      },
    });

  const handleDownload = async () => {
    if (!evaluationData) return;

    // =========================
    // LOAD LOGO
    // =========================
    const response = await fetch(logo);

    const logoBlob = await response.blob();

    const logoBuffer =
      await logoBlob.arrayBuffer();

    // =========================
    // PARSE DATA
    // =========================
    const data =
      typeof evaluationData === "string"
        ? JSON.parse(evaluationData)
        : evaluationData;

    const fileName = getFileName();

    // =========================
    // FEEDBACK
    // =========================
    const feedback = data?.Feedback || {};

    const alignedToRubric =
      feedback?.AlignedToRubric || {};

    const strengths =
      feedback?.Strengths || [];

    const improvements =
      feedback?.AreasForImprovement || [];

    const suggestions =
      feedback?.SuggestionsForRevision ||
      [];

    // =========================
    // CRITERIA
    // =========================
    const criteriaEntries =
      Object.entries(data).filter(
        ([key]) =>
          ![
            "TotalScore",
            "Percentage",
            "Grade",
            "OverallGrade",
            "Feedback",
          ].includes(key)
      );

    // =========================
    // DOC
    // =========================
    const doc = new Document({
      sections: [
        {
          children: [
            // =========================
            // LOGO
            // =========================
            new Paragraph({
              alignment:
                AlignmentType.LEFT,

              children: [
                new ImageRun({
                  type: "png",

                  data: new Uint8Array(
                    logoBuffer
                  ),

                  transformation: {
                    width: 180,
                    height: 60,
                  },
                }),
              ],

              spacing: {
                after: 250,
              },
            }),

            // =========================
            // TITLE
            // =========================
            new Paragraph({
              alignment:
                AlignmentType.CENTER,

              children: [
                new TextRun({
                  text: "Evaluation Report",
                  bold: true,
                  size: 40,
                  color: "000000",
                }),
              ],

              spacing: {
                after: 400,
              },
            }),

            // =========================
            // SUMMARY
            // =========================
            createHeading(
              "Grading Summary"
            ),

            new Paragraph({
              children: [
                new TextRun({
                  text: "Score: ",
                  bold: true,
                  color: "000000",
                }),

                new TextRun({
                  text:
                    data?.TotalScore ||
                    "N/A",

                  color: "000000",
                }),
              ],
            }),

            new Paragraph({
              children: [
                new TextRun({
                  text: "Grade: ",
                  bold: true,
                  color: "000000",
                }),

                new TextRun({
                  text:
                    data?.Grade || "N/A",

                  color: "000000",
                }),
              ],
            }),

            new Paragraph({
              children: [
                new TextRun({
                  text: "Overall: ",
                  bold: true,
                  color: "000000",
                }),

                new TextRun({
                  text:
                    data?.OverallGrade ||
                    "N/A",

                  color: "000000",
                }),
              ],

              spacing: {
                after: 100,
              },
            }),

            new Paragraph({
              children: [
                new TextRun({
                  text: "Percentage: ",
                  bold: true,
                  color: "000000",
                }),

                new TextRun({
                  text:
                    data?.Percentage ||
                    "N/A",

                  color: "000000",
                }),
              ],

              spacing: {
                after: 400,
              },
            }),

            // =========================
            // CRITERIA BREAKDOWN
            // =========================
            createHeading(
              "Criteria Breakdown"
            ),

            ...criteriaEntries.map(
              ([key, value]: any) =>
                new Paragraph({
                  children: [
                    new TextRun({
                      text: `${key}: `,
                      bold: true,
                      color: "000000",
                    }),

                    new TextRun({
                      text:
                        value?.toString() ||
                        "N/A",

                      color: "000000",
                    }),
                  ],

                  border: {
                    bottom: {
                      style:
                        BorderStyle.SINGLE,

                      size: 1,

                      color: "D3D3D3",
                    },
                  },

                  spacing: {
                    before: 100,
                    after: 100,
                  },
                })
            ),

            // =========================
            // FEEDBACK
            // =========================
            createHeading("Feedback"),

            ...Object.entries(
              alignedToRubric
            ).flatMap(
              ([key, value]: any) => [
                new Paragraph({
                  children: [
                    new TextRun({
                      text: key,
                      bold: true,
                      size: 28,
                      color: "000000",
                    }),
                  ],

                  spacing: {
                    before: 250,
                    after: 100,
                  },
                }),

                new Paragraph({
                  children: [
                    new TextRun({
                      text:
                        value?.toString() ||
                        "",

                      color: "000000",
                    }),
                  ],

                  spacing: {
                    after: 250,
                  },
                }),
              ]
            ),

            // =========================
            // STRENGTHS
            // =========================
            createHeading("Strengths"),

            ...strengths.map(
              (text: string) =>
                new Paragraph({
                  children: [
                    new TextRun({
                      text,
                      color: "000000",
                    }),
                  ],

                  bullet: {
                    level: 0,
                  },

                  spacing: {
                    after: 80,
                  },
                })
            ),

            // =========================
            // IMPROVEMENTS
            // =========================
            createHeading(
              "Areas for Improvement"
            ),

            ...improvements.map(
              (text: string) =>
                new Paragraph({
                  children: [
                    new TextRun({
                      text,
                      color: "000000",
                    }),
                  ],

                  bullet: {
                    level: 0,
                  },

                  spacing: {
                    after: 80,
                  },
                })
            ),

            // =========================
            // SUGGESTIONS
            // =========================
            createHeading("Suggestions"),

            ...suggestions.map(
              (text: string) =>
                new Paragraph({
                  children: [
                    new TextRun({
                      text,
                      color: "000000",
                    }),
                  ],

                  bullet: {
                    level: 0,
                  },

                  spacing: {
                    after: 80,
                  },
                })
            ),
          ],
        },
      ],
    });

    const blob = await Packer.toBlob(doc);

    saveAs(blob, `${fileName}.docx`);
  };

  return (
    <button
      className="btn btn-primary"
      onClick={handleDownload}
      style={{
        width: "fit-content",
      }}
    >
      Download Word
    </button>
  );
};

export default DownloadDocButton;
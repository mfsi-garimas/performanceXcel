import { Document, Packer, Paragraph, TextRun } from "docx";
import { saveAs } from "file-saver";
import getFileName from "./GenerateRandomFileName";

type Props = {
  targetRef: React.RefObject<HTMLDivElement | null>;
};

const DownloadDocButton = ({ targetRef }: Props) => {

  const handleDownload = async () => {
    if (!targetRef?.current) return;

    const fileName = getFileName();

    const textContent = targetRef.current.innerText;

    const lines = textContent.split("\n");

    const doc = new Document({
      sections: [
        {
          children: lines.map(
            (line) =>
              new Paragraph({
                children: [
                  new TextRun({
                    text: line,
                  }),
                ],
              })
          ),
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
      style={{ width: "fit-content" }}
    >
      Download Word
    </button>
  );
};

export default DownloadDocButton;
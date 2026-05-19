import html2pdf from "html2pdf.js";
import getFileName from "./GenerateRandomFileName";

type Props = {
  targetRef: React.RefObject<HTMLDivElement | null>;
};

const DownloadPDFButton = ({ targetRef }: Props) => {
  const handleDownload = async () => {
    if (!targetRef.current) return;

    const fileName = getFileName();

    const element = targetRef.current;

    const options = {
      margin: [10, 10, 10, 10] as [
        number,
        number,
        number,
        number
      ],

      filename: `${fileName}.pdf`,

      image: {
        type: "png" as const,
        quality: 1,
      },

      html2canvas: {
        scale: 2,
        useCORS: true,
        backgroundColor: "#ffffff",
      },

      jsPDF: {
        unit: "mm" as const,
        format: "a4" as const,
        orientation: "portrait" as const,
      },

      pagebreak: {
        mode: [ "css", "legacy"],
      },
    };

    await html2pdf()
      .set(options)
      .from(element)
      .save();
  };

  return (
    <button
      className="btn btn-primary"
      onClick={handleDownload}
      style={{
        width: "fit-content",
        marginRight: "10px",
      }}
    >
      Download PDF
    </button>
  );
};

export default DownloadPDFButton;
import React from "react";

interface Props {
  label: string;
  onChange: (file: File | null) => void;
}

const FileUpload: React.FC<Props> = ({ label, onChange }) => {
  return (
    <div style={{ marginBottom: "16px" }}>
      <label>{label}</label>
      <input
        type="file"
        onChange={(e) => onChange(e.target.files?.[0] || null)}
      />
    </div>
  );
};

export default FileUpload;
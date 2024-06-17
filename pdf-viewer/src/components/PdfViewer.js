import React from 'react';
import '../App.css'; // 스타일 파일을 임포트합니다

function PdfViewer({ fileUrl }) {
    return (
      <div className="PdfViewer-container">
        <iframe 
          src={`${fileUrl}#zoom=80`} 
          title="PDF Viewer"
          style={{ width: '100%', height: '100vh' }}
        >
          This browser does not support PDFs. Please download the PDF to view it: 
          <a href={fileUrl}>Download PDF</a>.
        </iframe>
      </div>
    );
  }

export default PdfViewer;

import React, { useState } from 'react';
import PdfViewer from './components/PdfViewer';
import Uploader from './components/Uploader';
import './App.css'; // 스타일 파일을 임포트합니다

function App() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);

  const handleFile1Select = (file) => {
    setFile1(URL.createObjectURL(file));
  };

  const handleFile2Select = (file) => {
    setFile2(URL.createObjectURL(file));
  };

  const bothFilesUploaded = file1 && file2;

  return (
    <div className="App">
      <div className="Uploader-container">
        <Uploader id="uploader1" onFileSelect={handleFile1Select} />
        <Uploader id="uploader2" onFileSelect={handleFile2Select} />
      </div>
      <header className="App-header">    
        {bothFilesUploaded && (
          <div className="PdfViewers">
            <PdfViewer fileUrl={file1} />
            <PdfViewer fileUrl={file2} />
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
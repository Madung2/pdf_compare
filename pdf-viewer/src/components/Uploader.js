import React, { useState } from 'react';
import styled from 'styled-components';

const UploaderContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 2px solid #333333;
  border-radius: 10px;
  background-color: #f9f9f9;
  width: 600px;
  margin: 20px auto;
`;

const Input = styled.input`
  display: none;
`;

const Label = styled.label`
  padding: 10px 20px;
  background-color: #333333;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  
  &:hover {
    background-color: #0056b3;
  }
`;

const FileName = styled.div`
  margin-top: 10px;
  font-size: 14px;
  color: #333333;
`;

const Uploader = ({ id, onFileSelect }) => {
  const [fileName, setFileName] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFileName(file.name);
      onFileSelect(file);
    }
  };

  return (
    <UploaderContainer>
      <Input 
        type="file" 
        id={id} 
        onChange={handleFileChange} 
      />
      <Label htmlFor={id}>Choose File</Label>
      {fileName && <FileName>Selected File: {fileName}</FileName>}
    </UploaderContainer>
  );
};

export default Uploader;

import React from 'react'
import DragDropFrame from './DragDropFrame'
import UploadFrame from './UploadFrame'

function ImportFiles(){
    return (
        <>
            <DragDropFrame width="800px" height="500px"/>
            <UploadFrame width="300px" height="700px"/>
        </>
    );
}

export default ImportFiles;
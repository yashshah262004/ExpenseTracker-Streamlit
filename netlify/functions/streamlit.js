const { spawn } = require('child_process');
const path = require('path');

exports.handler = async function(event, context) {
  // Start Streamlit
  const streamlit = spawn('streamlit', ['run', 'app.py']);
  
  // Handle stdout
  streamlit.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  // Handle stderr
  streamlit.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  return {
    statusCode: 200,
    body: JSON.stringify({ message: "Streamlit app started" })
  };
};
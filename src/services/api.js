// API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

/**
 * Uploads a medical report file and processes it
 * @param {File} file - The .txt file to upload
 * @returns {Promise<Object>} Response containing diagnosis
 */
export const processMedicalFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE_URL}/process_file`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to process file');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error processing file:', error);
    throw error;
  }
};

/**
 * Processes a medical report string
 * @param {string} reportContent - The medical report content as string
 * @returns {Promise<Object>} Response containing diagnosis
 */
export const processMedicalString = async (reportContent) => {
  try {
    const response = await fetch(`${API_BASE_URL}/process_string`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ report_content: reportContent }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to process report');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error processing string:', error);
    throw error;
  }
};


const API_BASE_URL = "http://127.0.0.1:5000/api";

export const fetchHelloMessage = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/hello`);
    if (!response.ok) {
      throw new Error("Failed to fetch data");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};

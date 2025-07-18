import React from 'react';

const TorahAISearch = () => {
  return (
    <div className="bg-gray-100 min-h-screen font-sans">
      <div className="max-w-3xl mx-auto my-8 bg-white rounded-lg shadow-md overflow-hidden">

        {/* Header */}
        <div className="p-6 border-b">
          <h1 className="text-2xl font-bold text-blue-800">TORAH AI</h1>
          <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition">
            + New Chat
          </button>
        </div>

        {/* Conversation History */}
        <div className="p-6 border-b">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-semibold text-gray-700">Conversation History</h3>
            <button className="text-sm text-blue-600 hover:underline">Clear All</button>
          </div>

          <div className="space-y-2">
            {[...Array(5)].map((_, i) => (
              <p key={i} className="text-gray-600 p-2 hover:bg-gray-50 rounded cursor-pointer">
                - What are the benefits of eating v...
              </p>
            ))}

            <h4 className="font-semibold text-gray-700 mt-4">Last 7 Days</h4>

            {[...Array(4)].map((_, i) => (
              <p key={i + 5} className="text-gray-600 p-2 hover:bg-gray-50 rounded cursor-pointer">
                - What are the benefits of eating v...
              </p>
            ))}

            <h4 className="font-semibold text-gray-700 mt-4">Settings</h4>
          </div>
        </div>

        {/* Question Section */}
        <div className="p-6 border-b">
          <p className="text-gray-700 font-medium">
            What is the difference between melacha and av melacha on Shabbat?
          </p>
        </div>

        {/* Answer Section */}
        <div className="p-6 border-b">
          <div className="mb-6">
            <p className="text-lg font-semibold mb-4">Great question!</p>
            <ul className="space-y-3 text-gray-700">
              <li className="font-bold">- Melacha vs. Av Melacha on Shabbat</li>
              <li className="ml-4">- Melacha <span className="hebrew-text">(מלאכה)</span></li>
              <li className="ml-8">- Definition: In halacha, a melacha refers to a category of creative labor that is prohibited on Shabbat.</li>
              <li className="ml-8">- These are not simply "work" in the modern sense (e.g., lifting something heavy), but rather specific types of constructive actions that were done in building the Mishkan (Tabernacle).</li>
              <li className="ml-8">- Example: Writing two letters, lighting a fire, or planting a seed are all melachot.</li>
              <li className="ml-4">- Av Melacha <span className="hebrew-text">(אב מלאכה)</span></li>
              <li className="ml-8">- Translation: "Primary category of labor"</li>
              <li className="ml-8">- There are 39 avot melacha (plural of av melacha), derived directly from the Torah.</li>
              <li className="ml-8">- These are the main archetypes of forbidden activities.</li>
              <li className="ml-8">- Each av melacha has related subcategories called toladot (offspring actions) that are also forbidden because they resemble or result from the same principle.</li>
              <li className="ml-4">- Relationship</li>
              <li className="ml-8">- Every av melacha is a melacha, but not every melacha is an av melacha.</li>
              <li className="ml-8">- Think of it like this:</li>
            </ul>
          </div>

          <div className="border-t pt-4">
            <p className="text-xs font-mono text-gray-500">CCCDHHJDMN2637872NDDM...</p>
            <p className="text-xs text-gray-500">PDF</p>
          </div>
        </div>

        {/* Search Section */}
        <div className="p-6">
          <div className="flex items-center border rounded-lg px-4 py-2">
            <input
              type="text"
              placeholder="Ask anything..."
              className="outline-none flex-grow"
            />
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </div>
          <p className="text-xs text-gray-500 mt-2 text-center">
            Torah AI will only respond with trusted Torah sources, not modern unsourced opinions or unreliable internet results
          </p>
        </div>

      </div>
    </div>
  );
};

export default TorahAISearch;

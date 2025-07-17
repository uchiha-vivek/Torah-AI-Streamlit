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

          <div className="space-y-2 max-h-60 overflow-y-auto">
            {[...Array(8)].map((_, i) => (
              <p key={i} className="text-gray-600 p-2 hover:bg-gray-50 rounded cursor-pointer">
                What are the benefits of eating v...
              </p>
            ))}

            <p className="text-xs text-gray-500 mt-4 mb-2">Last 7 Days</p>

            {[...Array(5)].map((_, i) => (
              <p key={`last-${i}`} className="text-gray-600 p-2 hover:bg-gray-50 rounded cursor-pointer">
                What are the benefits of eating v...
              </p>
            ))}
            <p className="text-gray-600 p-2 hover:bg-gray-50 rounded cursor-pointer">
              What is the difference between melacha and av melacha on Shabbat?
            </p>
          </div>
        </div>

        {/* Answer Section */}
        <div className="p-6 border-b">
          <div className="mb-6">
            <p className="text-lg font-semibold mb-4">Great question!</p>

            <h2 className="text-xl font-bold text-blue-800 mb-4">Melacha vs. Av Melacha on Shabbat</h2>

            <h3 className="font-bold mt-4">
              Melacha <span className="hebrew-text" style={{ direction: 'rtl', unicodeBidi: 'bidi-override' }}>(מלאכה)</span>
            </h3>
            <p className="text-gray-700 mt-2"><strong>Definition:</strong> In halacha, a melacha refers to a category of creative labor that is prohibited on Shabbat.</p>
            <p className="text-gray-700 mt-1">These are not simply "work" in the modern sense (e.g., lifting something heavy), but rather specific types of constructive actions that were done in building the Mishkan (Tabernacle).</p>
            <p className="text-gray-700 mt-1"><strong>Example:</strong> Writing two letters, lighting a fire, or planting a seed are all melachot.</p>

            <h3 className="font-bold mt-4">
              Av Melacha <span className="hebrew-text" style={{ direction: 'rtl', unicodeBidi: 'bidi-override' }}>(אב מלאכה)</span>
            </h3>
            <p className="text-gray-700 mt-2"><strong>Translation:</strong> "Primary category of labor"</p>
            <p className="text-gray-700 mt-1">There are 39 avot melacha (plural of av melacha), derived directly from the Torah.</p>
            <p className="text-gray-700 mt-1">These are the main archetypes of forbidden activities.</p>
            <p className="text-gray-700 mt-1">Each av melacha has related subcategories called toladot (offspring actions) that are also forbidden because they resemble or result from the same principle.</p>

            <h3 className="font-bold mt-4">Relationship</h3>
            <p className="text-gray-700 mt-2">Every av melacha is a melacha, but not every melacha is an av melacha.</p>
            <p className="text-gray-700 mt-1">Think of it like this:</p>
            <ul className="list-disc pl-5 mt-1 space-y-1 text-gray-700">
              <li><strong>Av Melacha</strong> = main category</li>
              <li><strong>Toladah</strong> = sub-action under that category</li>
              <li>Both are biblically prohibited (דאורייתא), but rabbinic rulings differ slightly in how each is treated.</li>
            </ul>

            <p className="text-gray-700 mt-2"><strong>Example:</strong></p>
            <p className="text-gray-700 mt-1"><strong>Av Melacha:</strong> Zore'a (sowing seeds)</p>
            <p className="text-gray-700 mt-1 ml-4">
              - <strong>Toladah:</strong> Watering plants (helps things grow — same effect as planting)
            </p>
          </div>

          {/* Search Box */}
          <div className="mt-6">
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
    </div>
  );
};

export default TorahAISearch;

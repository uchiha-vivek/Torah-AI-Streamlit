import React from 'react';

const TorahResearchAssistant = () => {
  return (
    <div className="bg-gray-50 min-h-screen font-sans">
      <div className="max-w-3xl mx-auto my-8 bg-white rounded-lg shadow-md overflow-hidden">

        {/* Header */}
        <div className="bg-blue-800 text-white p-6">
          <h1 className="text-2xl font-bold">
            Understand Advanced Torah Research, Accurately and Intelligently
          </h1>
          <p className="mt-2">
            Explore complex Talmudic concepts, compile comprehensive source lists, locate specific quotes, and discover connections between Torah topics, with verified citations from approved databases.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-2 gap-4 p-6 border-b">
          <div>
            <h3 className="font-semibold text-blue-800">Concept Explanation</h3>
            <p className="text-gray-600">- Explain complex Talmudic and Halachic concepts with citations</p>
          </div>
          <div>
            <h3 className="font-semibold text-blue-800">Find Sources</h3>
            <p className="text-gray-600">- Compile comprehensive source lists for research topics</p>
          </div>
          <div>
            <h3 className="font-semibold text-blue-800">Halachic Background</h3>
            <p className="text-gray-600">- What are the views on celebrating Yom Ha'atzmaut?</p>
          </div>
          <div>
            <h3 className="font-semibold text-blue-800">Topic Connections</h3>
            <p className="text-gray-600">- Explore relationships between different Torah topics</p>
          </div>
        </div>

        {/* Query Mode Selector */}
        <div className="p-6 border-b">
          <p className="text-gray-500 text-sm">Select a query mode above</p>
          <div className="mt-4 text-center">
            <p className="text-xl font-semibold">Shalom! What would you like to learn today?</p>
          </div>
        </div>

        {/* Search Bar */}
        <div className="p-6 border-b">
          <div className="flex items-center border rounded-lg px-4 py-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              type="text"
              placeholder="Search Torah Sources"
              className="ml-2 outline-none flex-grow"
            />
          </div>
        </div>

        {/* Footer Sections */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-6">
          <div>
            <h3 className="font-bold text-blue-800 mb-2">TORAH AI</h3>
            <p className="text-sm text-gray-600">
              AI-Powered Torah Research Assistant Providing Reliable Citations And Scholarly Analysis From Approved Databases.
            </p>
          </div>
          <div>
            <h3 className="font-bold text-blue-800 mb-2">SECURITY FEATURES</h3>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>- APPROVED DATABASE SOURCES ONLY</li>
              <li>- CITATION VERIFICATION SYSTEM</li>
              <li>- NO EXTERNAL INFORMATION MIXING</li>
              <li>- TRANSPARENT SOURCE ATTRIBUTION</li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold text-blue-800 mb-2">RESEARCH CAPABILITIES</h3>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>- TALMUDIC CONCEPT EXPLANATION</li>
              <li>- COMPREHENSIVE SOURCE COMPILATION</li>
              <li>- ORIGINAL QUOTE LOCATION</li>
              <li>- TOPIC CONNECTION ANALYSIS</li>
            </ul>
          </div>
        </div>

        {/* Disclaimer */}
        <div className="bg-gray-100 p-4 text-center text-xs text-gray-500">
          This Tool Provides Educational Information Only. For Halachic Rulings, Consult A Qualified Rabbi.
        </div>
      </div>
    </div>
  );
};

export default TorahResearchAssistant;

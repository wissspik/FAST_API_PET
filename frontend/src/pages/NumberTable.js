import React from 'react';

export default function NumberTable() {
  // Создаем массив чисел от 1 до 100
  const numbers = Array.from({ length: 100 }, (_, i) => i + 1);
  
  // Разбиваем массив на строки по 10 чисел
  const rows = [];
  for (let i = 0; i < numbers.length; i += 10) {
    rows.push(numbers.slice(i, i + 10));
  }

  return (
    <div className="p-8 w-full max-w-4xl">
      <h1 className="text-3xl mb-6 text-center">Таблица чисел</h1>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse border border-gray-300">
          <tbody>
            {rows.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {row.map((number) => (
                  <td 
                    key={number} 
                    className="border border-gray-300 p-3 text-center hover:bg-blue-100 transition-colors"
                  >
                    {number}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
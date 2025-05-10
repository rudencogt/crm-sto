export default function OrderCard({ item, onDelete }) {
    return (
      <div className="relative bg-white p-3 rounded-lg shadow-md border border-gray-200 text-sm">
        <button
          onClick={() => onDelete(item)}
          className="absolute top-1 right-2 text-gray-400 hover:text-red-500 text-lg leading-none"
          aria-label="Delete"
        >
          &times;
        </button>
        <div className="font-semibold text-gray-900 mb-1">
          {item.make} {item.model} <span className="text-xs text-gray-500">({item.plate})</span>
        </div>
        <div className="text-xs text-gray-600 mb-1">
          {item.phone}
        </div>
        <div className="text-gray-700 text-sm italic">
          {item.notes || "-"}
        </div>
      </div>
    );
  }
  
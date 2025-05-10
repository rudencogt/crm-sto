import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import SidebarLayout from "../../components/SidebarLayout";
import OrderCard from "../../components/OrderCard";
import CreateOrderOverlay from "../../components/CreateOrderOverlay";

function mapOrdersToBoard(orders) {
  const columns = {
    pending: {
      nameKey: "orders.pending",
      sections: {
        new: [],
        awaiting_parts_order: [],
        awaiting_parts_delivery: [],
      },
      color: "bg-yellow-100",
    },
    inProgress: {
      nameKey: "orders.in_progress",
      sections: {
        diagnostics: [],
        repair: [],
        precheck: [],
      },
      color: "bg-blue-100",
    },
    done: {
      nameKey: "orders.done",
      sections: {
        awaiting_client: [],
        done: [],
      },
      color: "bg-green-100",
    },
  };

  orders.forEach((order) => {
    for (const colKey in columns) {
      const sectionKeys = Object.keys(columns[colKey].sections);
      if (sectionKeys.includes(order.status)) {
        columns[colKey].sections[order.status].push(order);
        break;
      }
    }
  });

  return columns;
}

export default function Orders() {
  const [columns, setColumns] = useState({});
  const [showOverlay, setShowOverlay] = useState(false);
  const { t } = useTranslation();

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const res = await fetch("http://localhost:8000/orders", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!res.ok) throw new Error("Failed to load orders");
        const orders = await res.json();
        setColumns(mapOrdersToBoard(orders));
      } catch (err) {
        console.error("Error loading orders:", err);
      }
    };

    fetchOrders();
  }, []);

  const handleAddOrder = () => {
    setShowOverlay(true);
  };

  const handleCreateOrder = (newItem) => {
    setColumns((prev) => {
      const updated = { ...prev };
      if (updated.pending && updated.pending.sections.new) {
        updated.pending.sections.new.push({
          id: newItem.id,
          make: newItem.make,
          model: newItem.model,
          plate: newItem.plate,
          phone: newItem.phone,
          notes: newItem.notes,
          status: "new",
        });
      }
      return updated;
    });
  };

  const handleDeleteOrder = (itemToDelete) => {
    setColumns((prev) => {
      const updated = { ...prev };
      for (const colKey in updated) {
        const col = updated[colKey];
        const sectionKeys = Object.keys(col.sections);
        sectionKeys.forEach((sectionKey) => {
          col.sections[sectionKey] = col.sections[sectionKey].filter(
            (item) => item.id !== itemToDelete.id
          );
        });
      }
      return updated;
    });
  };

  return (
    <SidebarLayout>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">{t("dashboard.orders")}</h1>
        <button
          onClick={handleAddOrder}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          {t("orders.add_button")}
        </button>
      </div>
      <div className="flex gap-4">
        {Object.entries(columns).map(([key, col]) => (
          <div key={key} className="bg-white rounded shadow p-4 w-1/3">
            <h2 className="font-semibold text-gray-700 mb-4 text-lg">
              {t(col.nameKey)}
            </h2>
            <div className="space-y-4">
              {Object.entries(col.sections).map(([sectionKey, items]) => (
                <div key={sectionKey} className={`${col.color} p-2 rounded`}>
                  <h3 className="font-medium text-sm text-gray-700 mb-2">
                    {t(`orders.${sectionKey}`)}
                  </h3>
                  <div className="space-y-2">
                    {items.map((item) => (
                      <OrderCard
                        key={item.id}
                        item={item}
                        onDelete={handleDeleteOrder}
                      />
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {showOverlay && (
        <CreateOrderOverlay
          onClose={() => setShowOverlay(false)}
          onSubmit={handleCreateOrder}
        />
      )}
    </SidebarLayout>
  );
}

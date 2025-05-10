import { useState, useCallback, useEffect, useMemo } from "react";
import { useTranslation } from "react-i18next";
import CreatableSelect from "react-select/creatable";
import { ChevronDown, ChevronRight } from "lucide-react";

export default function CreateOrderOverlay({ onClose, onSubmit }) {
  const { t } = useTranslation();

  const [collapsed, setCollapsed] = useState({
    client: false,
    vehicle: true,
    order: true,
  });

  const [client, setClient] = useState({ phone: "", email: "", first_name: "", last_name: "" });
  const [vehicle, setVehicle] = useState({
    make: "",
    model: "",
    plate_number: "",
    vin: "",
    fuel_type: "",
    engine_volume: "",
    year: ""
  });
  const [order, setOrder] = useState({ notes: "", payment_method: "cash" });
  const [clientFound, setClientFound] = useState(null);
  const [carData, setCarData] = useState([]);

  useEffect(() => {
    fetch("/data/car-makes-models.json")
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setCarData(data);
        } else {
          console.error("Invalid car data format", data);
          setCarData([]);
        }
      })
      .catch(err => {
        console.error("Failed to load car data", err);
        setCarData([]);
      });
  }, []);

  const toggle = useCallback((key) => {
    setCollapsed(prev => ({ ...prev, [key]: !prev[key] }));
  }, []);

  const handleCheckClient = useCallback(async () => {
    try {
      const res = await fetch(`/clients/search?phone=${client.phone}`);
      if (!res.ok) throw new Error();
      const data = await res.json();
      setClient(prev => ({ ...prev, ...data }));
      setClientFound(true);
      setCollapsed(prev => ({ ...prev, client: false, vehicle: false }));
    } catch {
      setClientFound(false);
    }
  }, [client.phone]);

  const isValidEmail = (email) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  const handleCreateOrder = useCallback(async () => {
    if (client.email && !isValidEmail(client.email)) {
      alert(t("orders.invalid_email") || "Invalid email");
      return;
    }

    const token = localStorage.getItem("access_token");
    if (!token) {
      alert(t("auth.not_authenticated"));
      return;
    }

    const payload = { client, vehicle, order };

    try {
      const res = await fetch("http://localhost:8000/orders/full", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || t("orders.create_error"));
      }

      const createdOrder = await res.json();
      onSubmit({
        id: createdOrder.id,
        make: vehicle.make,
        model: vehicle.model,
        plate: vehicle.plate_number,
        phone: client.phone,
        notes: order.notes
      });
      onClose();
    } catch (error) {
      console.error("Order creation error:", error.message);
      alert(t("orders.create_error") + ": " + error.message);
    }
  }, [client, vehicle, order, onClose, onSubmit, t]);

  const Section = useCallback(({ id, title, children }) => (
    <div className="border-t pt-4 mt-4">
      <button
        type="button"
        onClick={() => toggle(id)}
        className="w-full flex items-center text-left font-semibold text-blue-600 mb-2"
      >
        {collapsed[id] ? <ChevronRight size={16} className="mr-2" /> : <ChevronDown size={16} className="mr-2" />}
        {title}
      </button>
      {!collapsed[id] && <div className="space-y-2 mb-2">{children}</div>}
    </div>
  ), [collapsed, toggle]);

  const makeOptions = useMemo(
    () => Array.isArray(carData) ? carData.map(entry => ({ value: entry.make, label: entry.make })) : [],
    [carData]
  );

  const modelOptions = useMemo(() => {
    const entry = carData.find(e => e.make === vehicle.make);
    return entry ? entry.models.map(m => ({ value: m, label: m })) : [];
  }, [carData, vehicle.make]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 overflow-y-auto">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-xl p-4 my-10">
        <h2 className="text-xl font-bold mb-4">{t("orders.create")}</h2>
        <form onSubmit={(e) => { e.preventDefault(); handleCreateOrder(); }}>
          <Section id="client" title={t("orders.client_section")}>
            <input
              type="text"
              name="phone"
              className="w-full border rounded p-2"
              placeholder={t("orders.phone")}
              value={client.phone}
              onChange={(e) => {
                const val = e.target.value.replace(/[^\d+]/g, "");
                setClient(prev => ({ ...prev, phone: val }));
              }}
              autoComplete="tel"
            />
            <button type="button" onClick={handleCheckClient} className="text-sm text-white bg-blue-600 px-3 py-1 rounded">
              {t("orders.check_client")}
            </button>
            {clientFound === false && <p className="text-red-500 text-sm">{t("orders.client_not_found")}</p>}
            <input
              type="email"
              name="email"
              className="w-full border rounded p-2"
              placeholder={t("orders.email")}
              value={client.email}
              onChange={(e) => {
                const val = e.target.value;
                const cleaned = val.replace(/[^a-zA-Z0-9@._+-]/g, "");
                setClient(prev => ({ ...prev, email: cleaned }));
              }}
              autoComplete="email"
            />
            <input
              type="text"
              name="first_name"
              className="w-full border rounded p-2"
              placeholder={t("orders.first_name")}
              value={client.first_name}
              onChange={(e) => {
                const val = e.target.value.replace(/[^A-Za-z\s'-]/g, "");
                setClient(prev => ({ ...prev, first_name: val }));
              }}
              autoComplete="given-name"
            />
            <input
              type="text"
              name="last_name"
              className="w-full border rounded p-2"
              placeholder={t("orders.last_name")}
              value={client.last_name}
              onChange={(e) => {
                const val = e.target.value.replace(/[^A-Za-z\s'-]/g, "");
                setClient(prev => ({ ...prev, last_name: val }));
              }}
              autoComplete="family-name"
            />
          </Section>

          <Section id="vehicle" title={t("orders.vehicle_section")}>
            <CreatableSelect
              isClearable
              options={makeOptions}
              value={vehicle.make ? { value: vehicle.make, label: vehicle.make } : null}
              onChange={(option) => {
                const make = option?.value || "";
                setVehicle((prev) => ({ ...prev, make, model: "" }));
              }}
              placeholder={t("orders.make")}
              className="react-select-container"
              classNamePrefix="react-select"
            />
            <CreatableSelect
              isClearable
              options={modelOptions}
              value={vehicle.model ? { value: vehicle.model, label: vehicle.model } : null}
              onChange={(option) => {
                const model = option?.value || "";
                setVehicle((prev) => ({ ...prev, model }));
              }}
              placeholder={t("orders.model")}
              className="react-select-container mt-2"
              classNamePrefix="react-select"
            />
            <input type="text" name="vin" className="w-full border rounded p-2" placeholder={t("orders.vin")}
              value={vehicle.vin} onChange={(e) => setVehicle(prev => ({ ...prev, vin: e.target.value }))} />
            <input type="text" name="plate_number" className="w-full border rounded p-2" placeholder={t("orders.plate_number")}
              value={vehicle.plate_number} onChange={(e) => setVehicle(prev => ({ ...prev, plate_number: e.target.value }))} />
            <input type="text" name="engine_volume" className="w-full border rounded p-2" placeholder={t("orders.engine_volume")}
              value={vehicle.engine_volume} onChange={(e) => setVehicle(prev => ({ ...prev, engine_volume: e.target.value }))} />
            <input type="text" name="year" className="w-full border rounded p-2" placeholder={t("orders.year")}
              value={vehicle.year} onChange={(e) => setVehicle(prev => ({ ...prev, year: e.target.value }))} />
            <select className="w-full border rounded p-2" value={vehicle.fuel_type}
              onChange={(e) => setVehicle(prev => ({ ...prev, fuel_type: e.target.value }))}>
              <option value="">{t("orders.fuel.select")}</option>
              <option value="petrol">{t("orders.fuel.petrol")}</option>
              <option value="diesel">{t("orders.fuel.diesel")}</option>
              <option value="hybrid">{t("orders.fuel.hybrid")}</option>
              <option value="electric">{t("orders.fuel.electric")}</option>
              <option value="lpg">{t("orders.fuel.lpg")}</option>
              <option value="other">{t("orders.fuel.other")}</option>
            </select>
          </Section>

          <Section id="order" title={t("orders.order_section")}>
            <textarea className="w-full border rounded p-2" placeholder={t("orders.notes")}
              value={order.notes} onChange={(e) => setOrder(prev => ({ ...prev, notes: e.target.value }))} />
          </Section>

          <div className="flex justify-end gap-2 mt-6">
            <button type="button" onClick={onClose} className="px-4 py-2 bg-gray-300 rounded">
              {t("common.cancel")}
            </button>
            <button type="submit" className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
              {t("orders.submit")}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

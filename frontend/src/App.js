import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import AdminLogin from "./pages/admin/Login";
import Users from "./pages/admin/Users";
import ClientLogin from "./pages/client/Login";
import Dashboard from "./pages/client/Dashboard";
import Orders from "./pages/client/Orders";
import PrivateRoute from "./components/PrivateRoute";
import ClientPrivateRoute from "./components/ClientPrivateRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Редирект с корня */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* Клиентская часть */}
        <Route path="/login" element={<ClientLogin />} />
        <Route
          path="/dashboard"
          element={
            <ClientPrivateRoute>
              <Dashboard />
            </ClientPrivateRoute>
          }
        />
        <Route
          path="/orders"
          element={
            <ClientPrivateRoute>
              <Orders />
            </ClientPrivateRoute>
          }
        />

        {/* Админская часть */}
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route
          path="/admin/users"
          element={
            <PrivateRoute>
              <Users />
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

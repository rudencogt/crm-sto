import { Navigate } from "react-router-dom";

export default function ClientPrivateRoute({ children }) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" replace />;
}

import { Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Dealers from './pages/Dealers';
import DealerDetail from './pages/DealerDetail';
import PostReview from './pages/PostReview';
import Login from './pages/Login';
import Register from './components/Register/Register';
import NotFound from './pages/NotFound';

export default function App() {
  return (
    <div className="app">
      <Header />
      <main className="main">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dealers" element={<Dealers />} />
          <Route path="/dealers/:state" element={<Dealers />} />
          <Route path="/dealer/:id" element={<DealerDetail />} />
          <Route path="/postreview/:id" element={<PostReview />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

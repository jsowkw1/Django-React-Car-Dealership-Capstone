import { useParams } from 'react-router-dom';
import DealerList from '../components/DealerList';

export default function Dealers() {
  const { state = 'All' } = useParams();
  return (
    <div className="container page">
      <DealerList state={decodeURIComponent(state)} />
    </div>
  );
}

import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Bar, Pie, Line } from 'react-chartjs-2';
import './QuantitativeAnalysis.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const QuantitativeAnalysis = ({ data }) => {
  if (!data) return null;

  const { marketSize, marketShare, regionalGrowth, priceEvolution } = data;

  // Configuration pour le graphique de taille de marché
  const marketSizeData = {
    labels: marketSize.labels,
    datasets: [
      {
        label: `Taille du marché (${marketSize.unit})`,
        data: marketSize.data,
        backgroundColor: 'rgba(0, 85, 184, 0.8)',
        borderColor: 'rgba(0, 85, 184, 1)',
        borderWidth: 2,
      }
    ]
  };

  const marketSizeOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Évolution de la taille du marché',
        font: {
          size: 16,
          weight: 'bold'
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return value.toLocaleString('fr-FR');
          }
        }
      }
    }
  };

  // Configuration pour le graphique de parts de marché
  const marketShareData = {
    labels: marketShare.labels,
    datasets: [
      {
        label: 'Part de marché (%)',
        data: marketShare.data,
        backgroundColor: marketShare.colors,
        borderWidth: 2,
        borderColor: '#fff'
      }
    ]
  };

  const marketShareOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'right',
      },
      title: {
        display: true,
        text: 'Parts de marché des principaux acteurs',
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `${context.label}: ${context.parsed}%`;
          }
        }
      }
    }
  };

  // Configuration pour la croissance régionale
  const regionalGrowthData = {
    labels: regionalGrowth.labels,
    datasets: [
      {
        label: 'Part du marché (%)',
        data: regionalGrowth.data,
        backgroundColor: 'rgba(0, 85, 184, 0.6)',
        borderColor: 'rgba(0, 85, 184, 1)',
        borderWidth: 2,
      },
      {
        label: 'Taux de croissance (%)',
        data: regionalGrowth.growth,
        backgroundColor: 'rgba(76, 175, 80, 0.6)',
        borderColor: 'rgba(76, 175, 80, 1)',
        borderWidth: 2,
      }
    ]
  };

  const regionalGrowthOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Distribution régionale et croissance',
        font: {
          size: 16,
          weight: 'bold'
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  // Configuration pour l'évolution des prix
  const priceEvolutionData = {
    labels: priceEvolution.labels,
    datasets: [
      {
        label: 'Prix moyen (€)',
        data: priceEvolution.avgPrice,
        borderColor: 'rgba(0, 85, 184, 1)',
        backgroundColor: 'rgba(0, 85, 184, 0.1)',
        tension: 0.4,
        fill: true,
        yAxisID: 'y',
      },
      {
        label: priceEvolution.batteryCost ? 'Coût batterie ($/kWh)' : 'Volume (millions)',
        data: priceEvolution.batteryCost || priceEvolution.transactions,
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.1)',
        tension: 0.4,
        fill: true,
        yAxisID: 'y1',
      }
    ]
  };

  const priceEvolutionOptions = {
    responsive: true,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Évolution des prix et volumes',
        font: {
          size: 16,
          weight: 'bold'
        }
      }
    },
    scales: {
      y: {
        type: 'linear',
        display: true,
        position: 'left',
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        grid: {
          drawOnChartArea: false,
        },
      },
    }
  };

  return (
    <div className="quantitative-analysis">
      <h2>📈 Analyse Quantitative</h2>
      
      <div className="charts-grid">
        <div className="chart-container">
          <Bar data={marketSizeData} options={marketSizeOptions} />
        </div>

        <div className="chart-container">
          <Pie data={marketShareData} options={marketShareOptions} />
        </div>

        <div className="chart-container full-width">
          <Bar data={regionalGrowthData} options={regionalGrowthOptions} />
        </div>

        <div className="chart-container full-width">
          <Line data={priceEvolutionData} options={priceEvolutionOptions} />
        </div>
      </div>

      <div className="key-metrics">
        <h3>📊 Indicateurs Clés</h3>
        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-icon">📈</div>
            <div className="metric-content">
              <span className="metric-label">Croissance annuelle</span>
              <span className="metric-value">+{((marketSize.data[marketSize.data.length - 1] / marketSize.data[marketSize.data.length - 2] - 1) * 100).toFixed(1)}%</span>
            </div>
          </div>
          
          <div className="metric-card">
            <div className="metric-icon">🏆</div>
            <div className="metric-content">
              <span className="metric-label">Leader du marché</span>
              <span className="metric-value">{marketShare.labels[0]}</span>
            </div>
          </div>
          
          <div className="metric-card">
            <div className="metric-icon">🌍</div>
            <div className="metric-content">
              <span className="metric-label">Principale région</span>
              <span className="metric-value">{regionalGrowth.labels[0]}</span>
            </div>
          </div>
          
          <div className="metric-card">
            <div className="metric-icon">💰</div>
            <div className="metric-content">
              <span className="metric-label">Taille actuelle</span>
              <span className="metric-value">{marketSize.data[marketSize.data.length - 1]} {marketSize.unit.split(' ')[1]}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuantitativeAnalysis;

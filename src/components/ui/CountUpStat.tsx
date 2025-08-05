import { useCountUp } from '@/hooks/useCountUp';

interface CountUpStatProps {
  value: string;
  className?: string;
}

const CountUpStat = ({ value, className }: CountUpStatProps) => {
  // Extract numeric value from string (e.g., "₿2,847" -> 2847)
  const numericValue = parseFloat(value.replace(/[^\d.]/g, ''));
  const prefix = value.match(/^[^\d]*/) ? value.match(/^[^\d]*/)?.[0] : '';
  const suffix = value.match(/[^\d]*$/) ? value.match(/[^\d]*$/)?.[0] : '';
  
  const isPercentage = value.includes('%');
  const hasComma = value.includes(',');
  
  const count = useCountUp({ 
    end: numericValue, 
    duration: 2500,
    decimals: isPercentage ? 1 : 0
  });
  
  const formatValue = (num: number) => {
    if (hasComma && num >= 1000) {
      return num.toLocaleString();
    }
    return isPercentage ? num.toFixed(1) : Math.floor(num).toString();
  };
  
  return (
    <div className={className}>
      {prefix}{formatValue(count)}{suffix}
    </div>
  );
};

export default CountUpStat;
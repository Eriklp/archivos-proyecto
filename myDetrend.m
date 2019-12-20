  function retorno = myDetrend(secuencia)
  t = 0:length(secuencia)-1;
  %x = 20*sin(t) + t.^2;
  y = detrend(secuencia,6);
  plot(t,y', ':k');
  legend('Input Data','Location','northwest') 
  end
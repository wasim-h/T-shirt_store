few_shots = [
  
    {
        'Question': "How many t-shirts do we have left for Nike in XS size and white color?",
        'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
    },
    
    
    {
        'Question': "What is the total value of our inventory for all S-size t-shirts?",
        'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE size = 'S'",
    },
    
  
    {
        'Question': "If we sell all Levi's T-shirts today with discounts, how much revenue will we make?",
        'SQLQuery': "SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi' group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id",
    },
    

    {
        'Question': "If we sell all Levi's T-shirts today without any discount, how much money will we make?",
        'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
    },
    
  
    {
        'Question': "What are all the different brands of t-shirts we carry?",
        'SQLQuery': "SELECT DISTINCT brand FROM t_shirts",
    },
    
   
    {
        'Question': "How many different types of white t-shirts are available?",
        'SQLQuery': "SELECT count(*) FROM t_shirts WHERE color = 'White'",
    }
]
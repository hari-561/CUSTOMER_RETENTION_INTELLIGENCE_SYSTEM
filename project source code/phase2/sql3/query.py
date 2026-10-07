from database import get_db,Base,engine,Session
from models import Customer,DimContract,DimPayment,FactCustomerAccount
from sqlalchemy import func, text
Base.metadata.create_all(bind = engine)

print("done.....")
db = Session()

# try:
#      result = db.query(Customer).all()

# except Exception as e:
#      print("found exe: " ,e)

# for row in result[:5]:
#      print(row.customer_id)
#      print(row.gender)

# try:
   
#      result = (
#           db.query(
#                DimContract.contract_name,
#                func.avg(FactCustomerAccount.churn).label("churn_rate")
#           )
#           .join(
#                DimContract,
#                FactCustomerAccount.contract_key == DimContract.contract_key
#           )
#           .group_by(DimContract.contract_name)
#           .order_by(func.avg(FactCustomerAccount.churn).desc())
#           .all()
#      )


# except Exception as e:
#      print("found exception:",e)

# print("query 1:",len(result))
# for contract, churn_rate in result:
#     print(contract, round(churn_rate * 100, 2), "%")

# try:
   
#      result = (
#           db.query(
#                DimPayment.payment_method,
#                func.avg(FactCustomerAccount.churn).label("churn_rate")
#           )
#           .join(
#                DimPayment,
#                FactCustomerAccount.payment_key == DimPayment.payment_key
#           )
#           .group_by(DimPayment.payment_method)
#           .order_by(func.avg(FactCustomerAccount.churn).desc())
#           .all()
#      )


# except Exception as e:
#      print("found exception:",e)

# print("query 2:",len(result))
# for payment_method, churn_rate in result:
#     print(payment_method, round(churn_rate * 100, 2), "%")

# print("\n")

# try:
#      result = (
#           db.query(
#                FactCustomerAccount.churn,
#                func.avg((FactCustomerAccount.monthly_charges)).label("monthly_charges")
#           )
#           .group_by(FactCustomerAccount.churn)
#      )

# except Exception as e:
#      print("found exception:",e)   


# for row in result:
#      print(row.churn, round(row.monthly_charges, 2))


# print("\n")


# # avg_charge = (
# # db.query(
# # func.avg(FactCustomerAccount.monthly_charges)))

# # print( "avg" , avg_charge)

# avg_charge = db.query(func.avg(FactCustomerAccount.monthly_charges)).scalar()
# try:
#      result = (
#           db.query(FactCustomerAccount)
#           .join(DimContract,
#                FactCustomerAccount.contract_key == DimContract.contract_key)

#           .filter(
#                DimContract .contract_name == "month-to-month",
#                FactCustomerAccount.tenure < 12,
#                FactCustomerAccount.monthly_charges > avg_charge
               
#           ).all()
#      )
# except Exception as e:
#      print("found exception in 68:",e)
# print("\n")

# print("query 4 ,count of customers:",len(result))

# for row in result[:5]:
#      print(row.customer_id, row.tenure, row.monthly_charges)


# try:
#      result = (db.query(
#           FactCustomerAccount
#      )
#      .filter(
#           FactCustomerAccount.churn == "True",
#           FactCustomerAccount.total_charges > 2000
#      ).all()
#      )
# except Exception as e:
#      print("found exception in 71:",e)

# print("\n")
# print("query 5,count of  High-value churned customers:",len(result))
# print("avg of them:",db.query(func.avg(FactCustomerAccount.total_charges)).filter(FactCustomerAccount.churn == "True", FactCustomerAccount.total_charges > 2000).scalar())



# result = (
#     db.query(
#         DimContract.contract_name.label("contract_type"),
#         func.round(
#             func.avg(FactCustomerAccount.monthly_charges), 2
#         ).label("avg_monthly_charges"),
#         func.round(
#             func.avg(FactCustomerAccount.tenure), 2
#         ).label("avg_tenure"),
#         func.round(
#             func.avg(FactCustomerAccount.churn) * 100, 2
#         ).label("churn_rate_pct")
#     )
#     .join(
#         DimContract,
#         FactCustomerAccount.contract_key == DimContract.contract_key
#     )
#     .group_by(DimContract.contract_name)
#     .order_by(
#         func.avg(FactCustomerAccount.churn).desc()
#     )
#     .all()
# )
# print("query 6:",len(result))
# for row in result:
#     print(
#         row.contract_type,
#         row.avg_monthly_charges,
#         row.avg_tenure,
#         row.churn_rate_pct
#     )

# query = text("""
# Insert into customer_ml_features (
#    customer_id,
#     gender,
#     senior_citizen,
#     partner,
#     dependent,
#     contract_type,
#     payment_method,
#     tenure,
#     monthly_charges,
#     total_charges,
#     services_count,
#     high_charge_flag,
#     is_long_term_contract,
#     auto_pay_flag,
#     churn)

#     select c.customer_id,
#     c.gender,
#     c.senior_citizen,
#     c.partner,
#     c.dependent,
#     dc.contract_name,
#     dp.payment_method,
#     fca.tenure,
#     fca.monthly_charges,
#     fca.total_charges,

#     (
#     COALESCE(stg.phone_service, 0)
#     + COALESCE(stg.multiple_lines, 0)
#     + COALESCE(stg.internet_service, 0)
#     + COALESCE(stg.online_security, 0)
#     + COALESCE(stg.online_backup, 0)
#     + COALESCE(stg.device_protection, 0)
#     + COALESCE(stg.tech_support, 0)
#     + COALESCE(stg.streaming_t_v, 0)
#     + COALESCE(stg.streaming_movies, 0) ) AS services,


#      case
#            when fca.monthly_charges > (select avg(monthly_charges)from fact_customer_account)
#                              then 1 else 0  end as high_charge_flag,
     
#      case 
#            when fca.tenure > 24 then 1 else 0 end as is_long_term_customer,

#      case  
#            when dp.payment_method like "%automatic%" then 1 else 0 end as auto_pay_flag,

#      fca.churn

#      from customers c
#      join fact_customer_account fca on c.customer_id = fca.customer_id
#      join dim_contract dc on fca.contract_key = dc.contract_key
#      join dim_payment dp on fca.payment_key = dp.payment_key     
#      join stg_customer_raw stg on c.customer_id = stg.customer_id

# """)

# try:
#      db.execute(query)
#      db.commit()
# except Exception as e:
#      db.rollback()
#      print("found exception in inserting:",e)



query = text("""

create view v_high_risk_customers 
as
select c.customer_id,c.tenure,c.monthly_charges,c.contract_type,
CONCAT(
        'High Risk because Contract = ', c.contract_type,
        ', Tenure = ', c.tenure, ' months (< 12)',
        ', Monthly Charges = ', c.monthly_charges,
        ' where avg = ', (SELECT AVG(monthly_charges) FROM customer_ml_features)
    ) AS risk_reason
from customer_ml_features c
where c.contract_type = "month-to-month" and 
c.tenure < 12 and   
c.monthly_charges > (select avg(monthly_charges) from customer_ml_features)
""")
try:
     db.execute(query)
     db.commit()
     print("view created successfully")
except Exception as e:
     db.rollback()
     print("found exception in creating view:",e)


# query = text ("""
#       SELECT
#     customer_id,
#      CONCAT(
#         'High Risk because Contract = ', c.contract_type,
#         ', Tenure = ', c.tenure, ' months (< 12)',
#         ', Monthly Charges = ', c.monthly_charges,
#         ' where avg = ', (SELECT AVG(monthly_charges) FROM customer_ml_features)
#     ) AS risk_reason
# FROM v_high_risk_customers c
# LIMIT 5;
# """)


# query = text ("""
#       SELECT
#     customer_id,
#      CONCAT(
#         'High Risk because Contract = ', contract_type,
#         ', Tenure = ', tenure, ' months (< 12)',
#         ', Monthly Charges = ', monthly_charges,
#         ' where avg = ', (SELECT AVG(monthly_charges) FROM customer_ml_features)
#     ) AS risk_reason
# FROM stg_customer_raw
# LIMIT 5;
# """)


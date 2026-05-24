Table ServiceRD {
  id integer [primary key]
  serviceRecordID integer
  serviceType string
  productUsed varchar
  quantity integer
  costs integer
  notes varcahr
}

Table Vehicle {
  id integer [primary key]
  vin integer
  year integer
  make string
  model string
  trim varchar
  engine_size varchar
  nickname varchar
}

Table ServiceRecord {
  id integer [primary key]
  vehicleID integer
  service_date integer
  mileage integer
  isDiy boolean
  serviceCenter varchar
  totalcosts integer
  notes varchar
}

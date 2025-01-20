g


Scenario purpose: Several product parameters need to be entered when new materials are created for plants. Create a set of default values for most commonly used product
attributes.

Script owner: Master Data

Pre-set Agree with different functions on default values to be used during initial material master setup.

Training doc: [https://communities.connect.te.com/sites/telag/Doc%20Library%20PUBLIC1/Material_Master_create_company_code_level.pptx](https://communities.connect.te.com/sites/telag/Doc%20Library%20PUBLIC1/Material_Master_create_company_code_level.pptx)

|Seq.|Test Condition|Processor Resp.|Transaction / function|Input Data Variable|Expected Result Variable|Actual result/Notes|
|---|---|---|---|---|---|---|
|10|Maintain Material Master Defaults|MM|ZDML|Open ZDML and enter: - Plant = your plant - Profit center → if defaults on profit center level = enter your profit center → if defaults on plant level = keep it blank Hit Enter on your keyboard to continue|ZDML screen displayed.||
|20|Maintain Sales org 1|MM|ZDML|Keep all attributes blank. These values are material specific.|||
||||||||


![](images/MM-0211-02---Create-MM-Default-Values-via-ZDML-(1).pdf-0-0.png)

![](images/MM-0211-02---Create-MM-Default-Values-via-ZDML-(1).pdf-0-1.png)

-----



g

|Seq.|Test Condition|Processor Resp.|Transaction / function|Input Data Variable|Expected Result Variable|Actual result/Notes|
|---|---|---|---|---|---|---|
|30|Maintain Sales org 2|MM|ZDML|- Matl stats grp = 1 - Acct asgnmt grp = 01 - Item cat.group = NORM These values will be used for the most of materials.|||
||||||||
|40|Maintain Sales: general / plant|MM|ZDML|- Trans.grp = 0001 (if maintainable) - Loading Grp = enter loading group according to warehouse setup These values will be used for the most of materials|||
||||||||
|50|Maintain Foreign Trade|MM|ZDML|- Export/import group = 01 - County of origin = enter initial value for country of origin. Correct one needs to be updated by trade compliance. These values will be used for the most of materials|||
||||||||
|60|Maintain Purchasing|MM|ZDML|- Purch Group = enter an initial value for purchasing group. Agree with purchasing team on initial value. - GR proc time = 1 (if needed)|||


![](images/MM-0211-02---Create-MM-Default-Values-via-ZDML-(1).pdf-1-0.png)

![](images/MM-0211-02---Create-MM-Default-Values-via-ZDML-(1).pdf-1-1.png)

-----



g

|Seq.|Test Condition|Processor Resp.|Transaction / function|Input Data Variable|Expected Result Variable|Actual result/Notes|
|---|---|---|---|---|---|---|
||||||||
|70|Maintain MRP1|MM|ZDML|- MRP group = enter initial MRP group agreed with planning - ABC indicator = C - Procurement = depending on the plant activities like TESOG, F can be entered as default value - Prod.stor.loc. = enter production storage location (if manufacturing plant level) - Stor.loc.EP = enter storage location for purchase order goods receipt - ScheMargin key = enter initial scheduling margin key value agreed with planning Values can be agreed with planning: - Planned delivery time - Inhouse production time Other date will need to be maintain material specific in ZCML.|||
||||||||


![](images/MM-0211-02---Create-MM-Default-Values-via-ZDML-(1).pdf-2-0.png)

-----



g

|Seq.|Test Condition|Processor Resp.|Transaction / function|Input Data Variable|Expected Result Variable|Actual result/Notes|
|---|---|---|---|---|---|---|
|80|Maintain MRP2|MM|ZDML|- MRP Type = ZH (agree with planning) - MRP Controller = enter initial MRP controller code agreed with planning - GIATP Extra % of Safety Stock = 100 - GIATP Call % of Safety Stock = 100 Other data need to be entered material specific in ZCML.|||
||||||||
|90|Maintain MRP3|MM|ZDML|- Mixed MRP = 1 - Splitting ind. = W - Availability check = agree with planning on initial value Values can be agreed with planning: - Total RL Time|||
||||||||
|100|Maintain Work Scheduling|MM|ZDML|- ProdProfile = agree with production on initial value - Primary Mfg Bldg = select from the list|||


![](images/MM-0211-02---Create-MM-Default-Values-via-ZDML-(1).pdf-3-0.png)

-----



g

|Seq.|Test Condition|Processor Resp.|Transaction / function|Input Data Variable|Expected Result Variable|Actual result/Notes|
|---|---|---|---|---|---|---|
||||||||
|110|Maintain Work Scheduling|MM|ZDML|If plant level is TESOG “No WS View” should be ticked ON to avoid that work scheduling view will be created for purchased parts on TESOG and you will be required to select primary mfg bldg.|||
|120|Maintain Quality Management|MM|ZDML|Depending on quality requirement either keep all fields empty or enter: - Create QM = tick ON - QM proc. Active = tick ON - QM control key = 0000|||
||||||||
|130|Maintain Accounting 1|MM|ZDML|Price unit = 1000 (agree with finance team) Standard price = 0,01 Currency = EUR (or your local currency if not EUR) LIFO/FIFO = OK|||
||||||||


![](images/MM-0211-02---Create-MM-Default-Values-via-ZDML-(1).pdf-4-0.png)

![](images/MM-0211-02---Create-MM-Default-Values-via-ZDML-(1).pdf-4-1.png)

-----



g

|Seq.|Test Condition|Processor Resp.|Transaction / function|Input Data Variable|Expected Result Variable|Actual result/Notes|
|---|---|---|---|---|---|---|
|140|Maintain Costing 1|MM|ZDML|Plant -sp.matl status = 03 Profit Center = your profit center Costing Lotsize = 1000 (the same of higher like Price Unit)|||
||||||||
|150|Maintain Costing 2|MM|ZDML|all fields should be empty|||
||||||||
|160|Maintain Storage|MM|ZDML|Enter all storage location which need to be used for all materials in your plant. Agree with warehouse team.|||
||||||||
|170|Maintain Warehouse 1|MM|ZDML|Keep all empty|||
||||||||


![](images/MM-0211-02---Create-MM-Default-Values-via-ZDML-(1).pdf-5-0.png)

![](images/MM-0211-02---Create-MM-Default-Values-via-ZDML-(1).pdf-5-1.png)

-----



g

|Seq.|Test Condition|Processor Resp.|Transaction / function|Input Data Variable|Expected Result Variable|Actual result/Notes|
|---|---|---|---|---|---|---|
|180|Maintain Material Master Defaults|MM|ZDML|Save changes.|||


![](images/MM-0211-02---Create-MM-Default-Values-via-ZDML-(1).pdf-6-0.png)

## Changes to this document
29 August 2019: Initial / WF


-----




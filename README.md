# OilProductionAndEQ
Our project try to mitigate the environmental impact of traditional energy production methods.

Traditional energy production methods can cause a significant negative impact on the environment and society. One example of negative outcomes is the occurrence of earthquakes resultant from the disposal of fluids in subsurface prevenient from these operations. Predicting the occurrence of these earthquakes and distinguishing it from naturally occurring ones is fundamental to companies looking to exploit subsurface energy resources. 

### Driving mechanuism of earthquakes

1. Natural Earthquakes    
An earthquake is caused by a sudden slip on a fault. The tectonic plates are always slowly moving, but they get stuck at their edges due to friction. When the stress on the edge overcomes the friction, there is an earthquake that releases energy in waves that travel through the earth's crust and cause the shaking that we feel.
2. Fluid Injection Induced Earthquakes    
Direct driving mechanisms: Pore-pressure increases in volume hydraulically connected to the injection wells. Pore-pressure increases, reducing the normal load on locked faults, thereby allowing sliding to occur.
Indirect driving mechanisms: The pore-pressure increase in the injection zone is expected to load the surrounding rock matrix and result in a fully coupled fluid-solid stress field. Elasticity is an effective means of transmitting forces to great distances. And therefore, the fully coupled poroelastic stress field can extend well beyond the fluid pressure increase in the hydraulically connected region.

## Workflow

1. Data Pre-processiong: Reorganized the data to make it easier to read.     
Integrated different years of earthquake data into a single table. Transferred the string of time into timestamp.     
Extracted the description information of each well from multiple well data files. Integrated all the well information into one table.    
Extracted the monthly production data of each well from multiple well data files. Consolidating all the production data into one table.   
The same processing is done for the injection data.   
After completing step a,b,c, the entire dataset was divided into four files.
Summed up the yearly production and injection, and reorganized the data for geographic analysis.

2. Buffer definition
3. Machine Learning

## Datasets

The data we used can be downloaded from: 

- earthquake data: [https://service.scedc.caltech.edu/ftp/catalogs/SCEC_DC/](https://service.scedc.caltech.edu/ftp/catalogs/SCEC_DC/)

- well location and production data: [https://www.dropbox.com/s/f65sopi8xvxt1f7/dataAllFields.zip?dl=0](https://www.dropbox.com/s/f65sopi8xvxt1f7/dataAllFields.zip?dl=0)

- oil field: [http://www.conservation.ca.gov/dog/maps/Pages/GISMapping2.aspx](http://www.conservation.ca.gov/dog/maps/Pages/GISMapping2.aspx)

## Contributors
|Name|Community|Contributions|E-mail|
|:--|:--|:--|:--|
|Tong Xiao|Tongji University|Defined oil field buffer, processed earthquake data, summed up production data of oil fields, conducted temporal feature engineering|pi620903@163.com|
|Shaoting Fu|Harbin Institute of Technology|Processed well location data with GIS, identified oil fields, identified earthquakes included in each oil field||
|Hansen Feng|Dalian University of Technology|Conducted temporal data analysis, conducted machine learning analysis||
|Yuhan Zhang|University of Melbourne|Conducted literature review and provided domain knowledge support||


## Acknowledgement
Thanks to Dr. Josimar A. Silva for his guidance on this project.

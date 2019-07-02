/*
	copy all files to location /var/lib/mysql-files/
*/

drop table Nutrition.nutrient_definition_src;
drop table Nutrition.nutrition_data_src;
drop table Nutrition.food_desc_src;
drop table Nutrition.food_group_src;
drop table Nutrition.weight_src;
drop table Nutrition.langual_factor_src;
drop table Nutrition.langual_factor_description_src;
drop table Nutrition.data_derivation_code_description_src;
drop table Nutrition.nutrition_data;


create table Nutrition.nutrition_data_src(nutrient_database_number varchar(1000) ,nutrient_number varchar(1000) ,nutrient_value varchar(1000) ,number_of_analyses varchar(1000) ,standard_error varchar(1000) ,type_of_data varchar(1000) ,derivation_code varchar(1000) ,reference_nutrient_database_number varchar(1000) ,additional_nutritional_mark varchar(1000) ,number_of_studies varchar(1000) ,minimum_value varchar(1000) ,maximum_value varchar(1000) ,degrees_of_freedom varchar(1000) ,lower_error_bound varchar(1000) ,upper_error_bound varchar(1000) ,statistical_comments varchar(1000) ,modified_date varchar(1000), PRIMARY KEY(nutrient_database_number,nutrient_number));

create table Nutrition.food_desc_src(nutrient_database_number varchar(1000),food_group_code varchar(1000),long_description varchar(1000),short_description varchar(1000),common_name varchar(1000),manufacturer_name varchar(1000),survey varchar(1000),refused_or_inedible_part_descrption varchar(1000),percentage_ofrefuse_by_weight varchar(1000),scientific_name varchar(1000),nitrogen_to_protein_converting_factor varchar(1000),protein_factor varchar(1000),fat_factor varchar(1000),carbohydrate_factor varchar(1000), PRIMARY KEY(nutrient_database_number));

create table Nutrition.food_group_src(food_group_code varchar(1000),food_group_description varchar(1000), PRIMARY KEY(food_group_code));

create table Nutrition.nutrient_definition_src(nutrient_number varchar(1000),units varchar(1000),tagname varchar(1000),nutrient_description varchar(1000),decimal_places_rounded varchar(1000),sr_legacy_sort_order varchar(1000),PRIMARY KEY(nutrient_number));



create table Nutrition.weight_src(nutrient_database_number varchar(1000),sequence_number varchar(1000),amount varchar(1000),measurement_description varchar(1000),weight_in_grams varchar(1000),number_of_data_points varchar(1000),standard_deviation varchar(1000),PRIMARY KEY(nutrient_database_number,sequence_number));

create table Nutrition.langual_factor_src(nutrient_database_number varchar(1000),langual_factor_code varchar(1000),PRIMARY KEY(nutrient_database_number,langual_factor_code));

create table Nutrition.langual_factor_description_src(langual_factor_code varchar(1000),langual_factor_description varchar(1000),PRIMARY KEY(langual_factor_code));

create table Nutrition.data_derivation_code_description_src(derivation_code varchar(1000),derivation_code_description varchar(1000),PRIMARY KEY(derivation_code) );

create table Nutrition.nutrition_data(nutrient_database_number varchar(250), long_description varchar(250), short_description varchar(250), food_group_description varchar(250), g__Protein__203 varchar(250), g__Total_lipid_fat__204 varchar(250), g__Carbohydrate_by_difference__205 varchar(250), g__Ash__207 varchar(250), kcal__Energy__208 varchar(250), g__Alcohol_ethyl__221 varchar(250), g__Water__255 varchar(250), mg__Caffeine__262 varchar(250), mg__Theobromine__263 varchar(250), kJ__Energy__268 varchar(250), g__Sugars_total__269 varchar(250), g__Fiber_total_dietary__291 varchar(250), mg__Calcium_Ca__301 varchar(250), mg__Iron_Fe__303 varchar(250), mg__Magnesium_Mg__304 varchar(250), mg__Phosphorus_P__305 varchar(250), mg__Potassium_K__306 varchar(250), mg__Sodium_Na__307 varchar(250), mg__Zinc_Zn__309 varchar(250), mg__Copper_Cu__312 varchar(250), mcg__Fluoride_F__313 varchar(250), mg__Manganese_Mn__315 varchar(250), mcg__Selenium_Se__317 varchar(250), IU__Vitamin_A_IU__318 varchar(250), mcg__Retinol__319 varchar(250), mcg__Vitamin_A_RAE__320 varchar(250), mcg__Carotene_beta__321 varchar(250), mcg__Carotene_alpha__322 varchar(250), mg__Vitamin_E_alpha_tocopherol__323 varchar(250), IU__Vitamin_D__324 varchar(250), mcg__Vitamin_D2_ergocalciferol__325 varchar(250), mcg__Vitamin_D3_cholecalciferol__326 varchar(250), mcg__Vitamin_D_D2_D3__328 varchar(250), mcg__Cryptoxanthin_beta__334 varchar(250), mcg__Lycopene__337 varchar(250), mcg__Lutein_zeaxanthin__338 varchar(250), mg__Tocopherol_beta__341 varchar(250), mg__Tocopherol_gamma__342 varchar(250), mg__Tocopherol_delta__343 varchar(250), mg__Tocotrienol_alpha__344 varchar(250), mg__Tocotrienol_beta__345 varchar(250), mg__Tocotrienol_gamma__346 varchar(250), mg__Tocotrienol_delta__347 varchar(250), mg__Vitamin_C_total_ascorbic_acid__401 varchar(250), mg__Thiamin__404 varchar(250), mg__Riboflavin__405 varchar(250), mg__Niacin__406 varchar(250), mg__Pantothenic_acid__410 varchar(250), mg__Vitamin_B_6__415 varchar(250), mcg__Folate_total__417 varchar(250), mcg__Vitamin_B_12__418 varchar(250), mg__Choline_total__421 varchar(250), mcg__Vitamin_K_phylloquinone__430 varchar(250), mcg__Folic_acid__431 varchar(250), mcg__Folate_food__432 varchar(250), mcg__Folate_DFE__435 varchar(250), mg__Betaine__454 varchar(250), g__Tryptophan__501 varchar(250), g__Threonine__502 varchar(250), g__Isoleucine__503 varchar(250), g__Leucine__504 varchar(250), g__Lysine__505 varchar(250), g__Methionine__506 varchar(250), g__Cystine__507 varchar(250), g__Phenylalanine__508 varchar(250), g__Tyrosine__509 varchar(250), g__Valine__510 varchar(250), g__Arginine__511 varchar(250), g__Histidine__512 varchar(250), g__Alanine__513 varchar(250), g__Aspartic_acid__514 varchar(250), g__Glutamic_acid__515 varchar(250), g__Glycine__516 varchar(250), g__Proline__517 varchar(250), g__Serine__518 varchar(250), mg__Vitamin_E_added__573 varchar(250), mcg__Vitamin_B_12_added__578 varchar(250), mg__Cholesterol__601 varchar(250), g__Fatty_acids_total_trans__605 varchar(250), g__Fatty_acids_total_saturated__606 varchar(250), g__4_isto_0__607 varchar(250), g__6_isto_0__608 varchar(250), g__8_isto_0__609 varchar(250), g__10_isto_0__610 varchar(250), g__12_isto_0__611 varchar(250), g__14_isto_0__612 varchar(250), g__16_isto_0__613 varchar(250), g__18_isto_0__614 varchar(250), g__20_isto_0__615 varchar(250), g__18_isto_1_undifferentiated__617 varchar(250), g__18_isto_2_undifferentiated__618 varchar(250), g__18_isto_3_undifferentiated__619 varchar(250), g__20_isto_4_undifferentiated__620 varchar(250), g__22_isto_6_n_3_DHA__621 varchar(250), g__16_isto_1_undifferentiated__626 varchar(250), g__18_isto_4__627 varchar(250), g__20_isto_1__628 varchar(250), g__20_isto_5_n_3_EPA__629 varchar(250), g__22_isto_1_undifferentiated__630 varchar(250), g__22_isto_5_n_3_DPA__631 varchar(250), mg__Stigmasterol__638 varchar(250), mg__Campesterol__639 varchar(250), mg__Beta_sitosterol__641 varchar(250), g__Fatty_acids_total_monounsaturated__645 varchar(250), g__Fatty_acids_total_polyunsaturated__646 varchar(250), g__17_isto_0__653 varchar(250), g__18_isto_1_t__663 varchar(250), g__18_isto_2_i__666 varchar(250), g__18_isto_2_CLAs__670 varchar(250), g__16_isto_1_c__673 varchar(250), g__18_isto_1_c__674 varchar(250), g__18_isto_2_n_6_c_c__675 varchar(250), g__Fatty_acids_total_trans_monoenoic__693 varchar(250), g__Fatty_acids_total_trans_polyenoic__695 varchar(250), g__18_isto_3_n_3_c_c_c_ALA__851 varchar(250), mcg__Menaquinone_4__428 varchar(250), mcg__Dihydrophylloquinone__429 varchar(250), g__22_isto_0__624 varchar(250), g__14_isto_1__625 varchar(250), g__15_isto_0__652 varchar(250), g__24_isto_0__654 varchar(250), g__16_isto_1_t__662 varchar(250), g__22_isto_1_t__664 varchar(250), g__18_isto_2_t_not_further_defined__665 varchar(250), g__24_isto_1_c__671 varchar(250), g__20_isto_2_n_6_c_c__672 varchar(250), g__22_isto_1_c__676 varchar(250), g__18_isto_3_n_6_c_c_c__685 varchar(250), g__17_isto_1__687 varchar(250), g__20_isto_3_undifferentiated__689 varchar(250), g__15_isto_1__697 varchar(250), g__20_isto_3_n_3__852 varchar(250), g__20_isto_3_n_6__853 varchar(250), g__18_isto_3i__856 varchar(250), g__22_isto_4__858 varchar(250), g__Sucrose__210 varchar(250), g__Glucose_dextrose__211 varchar(250), g__Fructose__212 varchar(250), g__Lactose__213 varchar(250), g__Maltose__214 varchar(250), g__Galactose__287 varchar(250), g__21_isto_5__857 varchar(250), g__Starch__209 varchar(250), g__Hydroxyproline__521 varchar(250), g__13_isto_0__696 varchar(250), g__18_isto_1_11_t_18_isto_1t_n_7__859 varchar(250), mg__Phytosterols__636 varchar(250), g__18_isto_2_t_t__669 varchar(250), g__20_isto_4_n_6__855 varchar(250), food_group_code varchar(250), common_name varchar(250), manufacturer_name varchar(250), survey varchar(250), refused_or_inedible_part_descrption varchar(250), percentage_ofrefuse_by_weight varchar(250), scientific_name varchar(250), nitrogen_to_protein_converting_factor varchar(250), protein_factor varchar(250), fat_factor varchar(250), carbohydrate_factor varchar(250), PRIMARY KEY (nutrient_database_number));


LOAD DATA INFILE '/var/lib/mysql-files/nutrition_data_src_1.txt' 
INTO TABLE Nutrition.nutrition_data_src 
FIELDS TERMINATED BY '^' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
LOAD DATA INFILE '/var/lib/mysql-files/nutrition_data_src_2.txt' 
INTO TABLE Nutrition.nutrition_data_src 
FIELDS TERMINATED BY '^' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
LOAD DATA INFILE '/var/lib/mysql-files/nutrition_data_src_3.txt' 
INTO TABLE Nutrition.nutrition_data_src 
FIELDS TERMINATED BY '^' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
LOAD DATA INFILE '/var/lib/mysql-files/nutrition_data_src_4.txt' 
INTO TABLE Nutrition.nutrition_data_src 
FIELDS TERMINATED BY '^' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA INFILE '/var/lib/mysql-files/food_desc_src.txt' 
INTO TABLE Nutrition.food_desc_src 
FIELDS TERMINATED BY '^' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA INFILE '/var/lib/mysql-files/data_derivation_code_description_src.txt' 
INTO TABLE Nutrition.data_derivation_code_description_src 
FIELDS TERMINATED BY '^' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA INFILE '/var/lib/mysql-files/food_group_src.txt' 
INTO TABLE Nutrition.food_group_src 
FIELDS TERMINATED BY '^' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA INFILE '/var/lib/mysql-files/langual_factor_description_src.txt' 
INTO TABLE Nutrition.langual_factor_description_src 
FIELDS TERMINATED BY '^' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA INFILE '/var/lib/mysql-files/langual_factor_src.txt' 
INTO TABLE Nutrition.langual_factor_src 
FIELDS TERMINATED BY '^' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA INFILE '/var/lib/mysql-files/nutrient_definition_src.txt' 
INTO TABLE Nutrition.nutrient_definition_src 
FIELDS TERMINATED BY '^' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA INFILE '/var/lib/mysql-files/weight_src.txt' 
INTO TABLE Nutrition.weight_src 
FIELDS TERMINATED BY '^' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

/*--------------------------------------------------------------------------------------------------------------------------------------*/
alter table Nutrition.nutrient_definition_src add column nutrient_name varchar(1000) after sr_legacy_sort_order;

update Nutrition.nutrient_definition_src 
set  nutrient_name =concat(units,'__',replace(replace(replace(replace(replace(replace(replace( replace(nutrient_description,':','_isto_'),'+',''),' ','_'),'-','_'),',','_'),')',''),'(',''),'__','_'),'__',nutrient_number);

alter table Nutrition.nutrition_data_src add column nutrient_name varchar(1000) after nutrient_number;

update Nutrition.nutrition_data_src t1 ,Nutrition.nutrient_definition_src t2 
set t1.nutrient_name =t2.nutrient_name 
where t1.nutrient_number=t2.nutrient_number;

alter table Nutrition.food_desc_src add column food_group_description varchar(1000) after food_group_code;

update Nutrition.food_desc_src t1 ,Nutrition.food_group_src t2 
set t1.food_group_description =t2.food_group_description 
where t1.food_group_code=t2.food_group_code;





insert into  nutrition_data select data.nutrient_database_number,data.long_description,data.short_description,data.food_group_description,
sum( if( nutrient_name = 'g__Protein__203', nutrient_value, 0 ) ) AS g__Protein__203,
sum( if( nutrient_name = 'g__Total_lipid_fat__204', nutrient_value, 0 ) ) AS g__Total_lipid_fat__204,
sum( if( nutrient_name = 'g__Carbohydrate_by_difference__205', nutrient_value, 0 ) ) AS g__Carbohydrate_by_difference__205,
sum( if( nutrient_name = 'g__Ash__207', nutrient_value, 0 ) ) AS g__Ash__207,
sum( if( nutrient_name = 'kcal__Energy__208', nutrient_value, 0 ) ) AS kcal__Energy__208,
sum( if( nutrient_name = 'g__Alcohol_ethyl__221', nutrient_value, 0 ) ) AS g__Alcohol_ethyl__221,
sum( if( nutrient_name = 'g__Water__255', nutrient_value, 0 ) ) AS g__Water__255,
sum( if( nutrient_name = 'mg__Caffeine__262', nutrient_value, 0 ) ) AS mg__Caffeine__262,
sum( if( nutrient_name = 'mg__Theobromine__263', nutrient_value, 0 ) ) AS mg__Theobromine__263,
sum( if( nutrient_name = 'kJ__Energy__268', nutrient_value, 0 ) ) AS kJ__Energy__268,
sum( if( nutrient_name = 'g__Sugars_total__269', nutrient_value, 0 ) ) AS g__Sugars_total__269,
sum( if( nutrient_name = 'g__Fiber_total_dietary__291', nutrient_value, 0 ) ) AS g__Fiber_total_dietary__291,
sum( if( nutrient_name = 'mg__Calcium_Ca__301', nutrient_value, 0 ) ) AS mg__Calcium_Ca__301,
sum( if( nutrient_name = 'mg__Iron_Fe__303', nutrient_value, 0 ) ) AS mg__Iron_Fe__303,
sum( if( nutrient_name = 'mg__Magnesium_Mg__304', nutrient_value, 0 ) ) AS mg__Magnesium_Mg__304,
sum( if( nutrient_name = 'mg__Phosphorus_P__305', nutrient_value, 0 ) ) AS mg__Phosphorus_P__305,
sum( if( nutrient_name = 'mg__Potassium_K__306', nutrient_value, 0 ) ) AS mg__Potassium_K__306,
sum( if( nutrient_name = 'mg__Sodium_Na__307', nutrient_value, 0 ) ) AS mg__Sodium_Na__307,
sum( if( nutrient_name = 'mg__Zinc_Zn__309', nutrient_value, 0 ) ) AS mg__Zinc_Zn__309,
sum( if( nutrient_name = 'mg__Copper_Cu__312', nutrient_value, 0 ) ) AS mg__Copper_Cu__312,
sum( if( nutrient_name = 'mcg__Fluoride_F__313', nutrient_value, 0 ) ) AS mcg__Fluoride_F__313,
sum( if( nutrient_name = 'mg__Manganese_Mn__315', nutrient_value, 0 ) ) AS mg__Manganese_Mn__315,
sum( if( nutrient_name = 'mcg__Selenium_Se__317', nutrient_value, 0 ) ) AS mcg__Selenium_Se__317,
sum( if( nutrient_name = 'IU__Vitamin_A_IU__318', nutrient_value, 0 ) ) AS IU__Vitamin_A_IU__318,
sum( if( nutrient_name = 'mcg__Retinol__319', nutrient_value, 0 ) ) AS mcg__Retinol__319,
sum( if( nutrient_name = 'mcg__Vitamin_A_RAE__320', nutrient_value, 0 ) ) AS mcg__Vitamin_A_RAE__320,
sum( if( nutrient_name = 'mcg__Carotene_beta__321', nutrient_value, 0 ) ) AS mcg__Carotene_beta__321,
sum( if( nutrient_name = 'mcg__Carotene_alpha__322', nutrient_value, 0 ) ) AS mcg__Carotene_alpha__322,
sum( if( nutrient_name = 'mg__Vitamin_E_alpha_tocopherol__323', nutrient_value, 0 ) ) AS mg__Vitamin_E_alpha_tocopherol__323,
sum( if( nutrient_name = 'IU__Vitamin_D__324', nutrient_value, 0 ) ) AS IU__Vitamin_D__324,
sum( if( nutrient_name = 'mcg__Vitamin_D2_ergocalciferol__325', nutrient_value, 0 ) ) AS mcg__Vitamin_D2_ergocalciferol__325,
sum( if( nutrient_name = 'mcg__Vitamin_D3_cholecalciferol__326', nutrient_value, 0 ) ) AS mcg__Vitamin_D3_cholecalciferol__326,
sum( if( nutrient_name = 'mcg__Vitamin_D_D2_D3__328', nutrient_value, 0 ) ) AS mcg__Vitamin_D_D2_D3__328,
sum( if( nutrient_name = 'mcg__Cryptoxanthin_beta__334', nutrient_value, 0 ) ) AS mcg__Cryptoxanthin_beta__334,
sum( if( nutrient_name = 'mcg__Lycopene__337', nutrient_value, 0 ) ) AS mcg__Lycopene__337,
sum( if( nutrient_name = 'mcg__Lutein_zeaxanthin__338', nutrient_value, 0 ) ) AS mcg__Lutein_zeaxanthin__338,
sum( if( nutrient_name = 'mg__Tocopherol_beta__341', nutrient_value, 0 ) ) AS mg__Tocopherol_beta__341,
sum( if( nutrient_name = 'mg__Tocopherol_gamma__342', nutrient_value, 0 ) ) AS mg__Tocopherol_gamma__342,
sum( if( nutrient_name = 'mg__Tocopherol_delta__343', nutrient_value, 0 ) ) AS mg__Tocopherol_delta__343,
sum( if( nutrient_name = 'mg__Tocotrienol_alpha__344', nutrient_value, 0 ) ) AS mg__Tocotrienol_alpha__344,
sum( if( nutrient_name = 'mg__Tocotrienol_beta__345', nutrient_value, 0 ) ) AS mg__Tocotrienol_beta__345,
sum( if( nutrient_name = 'mg__Tocotrienol_gamma__346', nutrient_value, 0 ) ) AS mg__Tocotrienol_gamma__346,
sum( if( nutrient_name = 'mg__Tocotrienol_delta__347', nutrient_value, 0 ) ) AS mg__Tocotrienol_delta__347,
sum( if( nutrient_name = 'mg__Vitamin_C_total_ascorbic_acid__401', nutrient_value, 0 ) ) AS mg__Vitamin_C_total_ascorbic_acid__401,
sum( if( nutrient_name = 'mg__Thiamin__404', nutrient_value, 0 ) ) AS mg__Thiamin__404,
sum( if( nutrient_name = 'mg__Riboflavin__405', nutrient_value, 0 ) ) AS mg__Riboflavin__405,
sum( if( nutrient_name = 'mg__Niacin__406', nutrient_value, 0 ) ) AS mg__Niacin__406,
sum( if( nutrient_name = 'mg__Pantothenic_acid__410', nutrient_value, 0 ) ) AS mg__Pantothenic_acid__410,
sum( if( nutrient_name = 'mg__Vitamin_B_6__415', nutrient_value, 0 ) ) AS mg__Vitamin_B_6__415,
sum( if( nutrient_name = 'mcg__Folate_total__417', nutrient_value, 0 ) ) AS mcg__Folate_total__417,
sum( if( nutrient_name = 'mcg__Vitamin_B_12__418', nutrient_value, 0 ) ) AS mcg__Vitamin_B_12__418,
sum( if( nutrient_name = 'mg__Choline_total__421', nutrient_value, 0 ) ) AS mg__Choline_total__421,
sum( if( nutrient_name = 'mcg__Vitamin_K_phylloquinone__430', nutrient_value, 0 ) ) AS mcg__Vitamin_K_phylloquinone__430,
sum( if( nutrient_name = 'mcg__Folic_acid__431', nutrient_value, 0 ) ) AS mcg__Folic_acid__431,
sum( if( nutrient_name = 'mcg__Folate_food__432', nutrient_value, 0 ) ) AS mcg__Folate_food__432,
sum( if( nutrient_name = 'mcg__Folate_DFE__435', nutrient_value, 0 ) ) AS mcg__Folate_DFE__435,
sum( if( nutrient_name = 'mg__Betaine__454', nutrient_value, 0 ) ) AS mg__Betaine__454,
sum( if( nutrient_name = 'g__Tryptophan__501', nutrient_value, 0 ) ) AS g__Tryptophan__501,
sum( if( nutrient_name = 'g__Threonine__502', nutrient_value, 0 ) ) AS g__Threonine__502,
sum( if( nutrient_name = 'g__Isoleucine__503', nutrient_value, 0 ) ) AS g__Isoleucine__503,
sum( if( nutrient_name = 'g__Leucine__504', nutrient_value, 0 ) ) AS g__Leucine__504,
sum( if( nutrient_name = 'g__Lysine__505', nutrient_value, 0 ) ) AS g__Lysine__505,
sum( if( nutrient_name = 'g__Methionine__506', nutrient_value, 0 ) ) AS g__Methionine__506,
sum( if( nutrient_name = 'g__Cystine__507', nutrient_value, 0 ) ) AS g__Cystine__507,
sum( if( nutrient_name = 'g__Phenylalanine__508', nutrient_value, 0 ) ) AS g__Phenylalanine__508,
sum( if( nutrient_name = 'g__Tyrosine__509', nutrient_value, 0 ) ) AS g__Tyrosine__509,
sum( if( nutrient_name = 'g__Valine__510', nutrient_value, 0 ) ) AS g__Valine__510,
sum( if( nutrient_name = 'g__Arginine__511', nutrient_value, 0 ) ) AS g__Arginine__511,
sum( if( nutrient_name = 'g__Histidine__512', nutrient_value, 0 ) ) AS g__Histidine__512,
sum( if( nutrient_name = 'g__Alanine__513', nutrient_value, 0 ) ) AS g__Alanine__513,
sum( if( nutrient_name = 'g__Aspartic_acid__514', nutrient_value, 0 ) ) AS g__Aspartic_acid__514,
sum( if( nutrient_name = 'g__Glutamic_acid__515', nutrient_value, 0 ) ) AS g__Glutamic_acid__515,
sum( if( nutrient_name = 'g__Glycine__516', nutrient_value, 0 ) ) AS g__Glycine__516,
sum( if( nutrient_name = 'g__Proline__517', nutrient_value, 0 ) ) AS g__Proline__517,
sum( if( nutrient_name = 'g__Serine__518', nutrient_value, 0 ) ) AS g__Serine__518,
sum( if( nutrient_name = 'mg__Vitamin_E_added__573', nutrient_value, 0 ) ) AS mg__Vitamin_E_added__573,
sum( if( nutrient_name = 'mcg__Vitamin_B_12_added__578', nutrient_value, 0 ) ) AS mcg__Vitamin_B_12_added__578,
sum( if( nutrient_name = 'mg__Cholesterol__601', nutrient_value, 0 ) ) AS mg__Cholesterol__601,
sum( if( nutrient_name = 'g__Fatty_acids_total_trans__605', nutrient_value, 0 ) ) AS g__Fatty_acids_total_trans__605,
sum( if( nutrient_name = 'g__Fatty_acids_total_saturated__606', nutrient_value, 0 ) ) AS g__Fatty_acids_total_saturated__606,
sum( if( nutrient_name = 'g__4_isto_0__607', nutrient_value, 0 ) ) AS g__4_isto_0__607,
sum( if( nutrient_name = 'g__6_isto_0__608', nutrient_value, 0 ) ) AS g__6_isto_0__608,
sum( if( nutrient_name = 'g__8_isto_0__609', nutrient_value, 0 ) ) AS g__8_isto_0__609,
sum( if( nutrient_name = 'g__10_isto_0__610', nutrient_value, 0 ) ) AS g__10_isto_0__610,
sum( if( nutrient_name = 'g__12_isto_0__611', nutrient_value, 0 ) ) AS g__12_isto_0__611,
sum( if( nutrient_name = 'g__14_isto_0__612', nutrient_value, 0 ) ) AS g__14_isto_0__612,
sum( if( nutrient_name = 'g__16_isto_0__613', nutrient_value, 0 ) ) AS g__16_isto_0__613,
sum( if( nutrient_name = 'g__18_isto_0__614', nutrient_value, 0 ) ) AS g__18_isto_0__614,
sum( if( nutrient_name = 'g__20_isto_0__615', nutrient_value, 0 ) ) AS g__20_isto_0__615,
sum( if( nutrient_name = 'g__18_isto_1_undifferentiated__617', nutrient_value, 0 ) ) AS g__18_isto_1_undifferentiated__617,
sum( if( nutrient_name = 'g__18_isto_2_undifferentiated__618', nutrient_value, 0 ) ) AS g__18_isto_2_undifferentiated__618,
sum( if( nutrient_name = 'g__18_isto_3_undifferentiated__619', nutrient_value, 0 ) ) AS g__18_isto_3_undifferentiated__619,
sum( if( nutrient_name = 'g__20_isto_4_undifferentiated__620', nutrient_value, 0 ) ) AS g__20_isto_4_undifferentiated__620,
sum( if( nutrient_name = 'g__22_isto_6_n_3_DHA__621', nutrient_value, 0 ) ) AS g__22_isto_6_n_3_DHA__621,
sum( if( nutrient_name = 'g__16_isto_1_undifferentiated__626', nutrient_value, 0 ) ) AS g__16_isto_1_undifferentiated__626,
sum( if( nutrient_name = 'g__18_isto_4__627', nutrient_value, 0 ) ) AS g__18_isto_4__627,
sum( if( nutrient_name = 'g__20_isto_1__628', nutrient_value, 0 ) ) AS g__20_isto_1__628,
sum( if( nutrient_name = 'g__20_isto_5_n_3_EPA__629', nutrient_value, 0 ) ) AS g__20_isto_5_n_3_EPA__629,
sum( if( nutrient_name = 'g__22_isto_1_undifferentiated__630', nutrient_value, 0 ) ) AS g__22_isto_1_undifferentiated__630,
sum( if( nutrient_name = 'g__22_isto_5_n_3_DPA__631', nutrient_value, 0 ) ) AS g__22_isto_5_n_3_DPA__631,
sum( if( nutrient_name = 'mg__Stigmasterol__638', nutrient_value, 0 ) ) AS mg__Stigmasterol__638,
sum( if( nutrient_name = 'mg__Campesterol__639', nutrient_value, 0 ) ) AS mg__Campesterol__639,
sum( if( nutrient_name = 'mg__Beta_sitosterol__641', nutrient_value, 0 ) ) AS mg__Beta_sitosterol__641,
sum( if( nutrient_name = 'g__Fatty_acids_total_monounsaturated__645', nutrient_value, 0 ) ) AS g__Fatty_acids_total_monounsaturated__645,
sum( if( nutrient_name = 'g__Fatty_acids_total_polyunsaturated__646', nutrient_value, 0 ) ) AS g__Fatty_acids_total_polyunsaturated__646,
sum( if( nutrient_name = 'g__17_isto_0__653', nutrient_value, 0 ) ) AS g__17_isto_0__653,
sum( if( nutrient_name = 'g__18_isto_1_t__663', nutrient_value, 0 ) ) AS g__18_isto_1_t__663,
sum( if( nutrient_name = 'g__18_isto_2_i__666', nutrient_value, 0 ) ) AS g__18_isto_2_i__666,
sum( if( nutrient_name = 'g__18_isto_2_CLAs__670', nutrient_value, 0 ) ) AS g__18_isto_2_CLAs__670,
sum( if( nutrient_name = 'g__16_isto_1_c__673', nutrient_value, 0 ) ) AS g__16_isto_1_c__673,
sum( if( nutrient_name = 'g__18_isto_1_c__674', nutrient_value, 0 ) ) AS g__18_isto_1_c__674,
sum( if( nutrient_name = 'g__18_isto_2_n_6_c_c__675', nutrient_value, 0 ) ) AS g__18_isto_2_n_6_c_c__675,
sum( if( nutrient_name = 'g__Fatty_acids_total_trans_monoenoic__693', nutrient_value, 0 ) ) AS g__Fatty_acids_total_trans_monoenoic__693,
sum( if( nutrient_name = 'g__Fatty_acids_total_trans_polyenoic__695', nutrient_value, 0 ) ) AS g__Fatty_acids_total_trans_polyenoic__695,
sum( if( nutrient_name = 'g__18_isto_3_n_3_c_c_c_ALA__851', nutrient_value, 0 ) ) AS g__18_isto_3_n_3_c_c_c_ALA__851,
sum( if( nutrient_name = 'mcg__Menaquinone_4__428', nutrient_value, 0 ) ) AS mcg__Menaquinone_4__428,
sum( if( nutrient_name = 'mcg__Dihydrophylloquinone__429', nutrient_value, 0 ) ) AS mcg__Dihydrophylloquinone__429,
sum( if( nutrient_name = 'g__22_isto_0__624', nutrient_value, 0 ) ) AS g__22_isto_0__624,
sum( if( nutrient_name = 'g__14_isto_1__625', nutrient_value, 0 ) ) AS g__14_isto_1__625,
sum( if( nutrient_name = 'g__15_isto_0__652', nutrient_value, 0 ) ) AS g__15_isto_0__652,
sum( if( nutrient_name = 'g__24_isto_0__654', nutrient_value, 0 ) ) AS g__24_isto_0__654,
sum( if( nutrient_name = 'g__16_isto_1_t__662', nutrient_value, 0 ) ) AS g__16_isto_1_t__662,
sum( if( nutrient_name = 'g__22_isto_1_t__664', nutrient_value, 0 ) ) AS g__22_isto_1_t__664,
sum( if( nutrient_name = 'g__18_isto_2_t_not_further_defined__665', nutrient_value, 0 ) ) AS g__18_isto_2_t_not_further_defined__665,
sum( if( nutrient_name = 'g__24_isto_1_c__671', nutrient_value, 0 ) ) AS g__24_isto_1_c__671,
sum( if( nutrient_name = 'g__20_isto_2_n_6_c_c__672', nutrient_value, 0 ) ) AS g__20_isto_2_n_6_c_c__672,
sum( if( nutrient_name = 'g__22_isto_1_c__676', nutrient_value, 0 ) ) AS g__22_isto_1_c__676,
sum( if( nutrient_name = 'g__18_isto_3_n_6_c_c_c__685', nutrient_value, 0 ) ) AS g__18_isto_3_n_6_c_c_c__685,
sum( if( nutrient_name = 'g__17_isto_1__687', nutrient_value, 0 ) ) AS g__17_isto_1__687,
sum( if( nutrient_name = 'g__20_isto_3_undifferentiated__689', nutrient_value, 0 ) ) AS g__20_isto_3_undifferentiated__689,
sum( if( nutrient_name = 'g__15_isto_1__697', nutrient_value, 0 ) ) AS g__15_isto_1__697,
sum( if( nutrient_name = 'g__20_isto_3_n_3__852', nutrient_value, 0 ) ) AS g__20_isto_3_n_3__852,
sum( if( nutrient_name = 'g__20_isto_3_n_6__853', nutrient_value, 0 ) ) AS g__20_isto_3_n_6__853,
sum( if( nutrient_name = 'g__18_isto_3i__856', nutrient_value, 0 ) ) AS g__18_isto_3i__856,
sum( if( nutrient_name = 'g__22_isto_4__858', nutrient_value, 0 ) ) AS g__22_isto_4__858,
sum( if( nutrient_name = 'g__Sucrose__210', nutrient_value, 0 ) ) AS g__Sucrose__210,
sum( if( nutrient_name = 'g__Glucose_dextrose__211', nutrient_value, 0 ) ) AS g__Glucose_dextrose__211,
sum( if( nutrient_name = 'g__Fructose__212', nutrient_value, 0 ) ) AS g__Fructose__212,
sum( if( nutrient_name = 'g__Lactose__213', nutrient_value, 0 ) ) AS g__Lactose__213,
sum( if( nutrient_name = 'g__Maltose__214', nutrient_value, 0 ) ) AS g__Maltose__214,
sum( if( nutrient_name = 'g__Galactose__287', nutrient_value, 0 ) ) AS g__Galactose__287,
sum( if( nutrient_name = 'g__21_isto_5__857', nutrient_value, 0 ) ) AS g__21_isto_5__857,
sum( if( nutrient_name = 'g__Starch__209', nutrient_value, 0 ) ) AS g__Starch__209,
sum( if( nutrient_name = 'g__Hydroxyproline__521', nutrient_value, 0 ) ) AS g__Hydroxyproline__521,
sum( if( nutrient_name = 'g__13_isto_0__696', nutrient_value, 0 ) ) AS g__13_isto_0__696,
sum( if( nutrient_name = 'g__18_isto_1_11_t_18_isto_1t_n_7__859', nutrient_value, 0 ) ) AS g__18_isto_1_11_t_18_isto_1t_n_7__859,
sum( if( nutrient_name = 'mg__Phytosterols__636', nutrient_value, 0 ) ) AS mg__Phytosterols__636,
sum( if( nutrient_name = 'g__18_isto_2_t_t__669', nutrient_value, 0 ) ) AS g__18_isto_2_t_t__669,
sum( if( nutrient_name = 'g__20_isto_4_n_6__855', nutrient_value, 0 ) ) AS g__20_isto_4_n_6__855,
data.food_group_code,data.common_name,data.manufacturer_name,data.survey,data.refused_or_inedible_part_descrption,data.percentage_ofrefuse_by_weight,data.scientific_name,data.nitrogen_to_protein_converting_factor,data.protein_factor,data.fat_factor,data.carbohydrate_factor from (select a.nutrient_database_number,b.long_description,b.short_description,b.food_group_description,a.nutrient_name,a.nutrient_value,b.food_group_code,b.common_name,b.manufacturer_name,b.survey,b.refused_or_inedible_part_descrption,b.percentage_ofrefuse_by_weight,b.scientific_name,b.nitrogen_to_protein_converting_factor,b.protein_factor,b.fat_factor,b.carbohydrate_factor from nutrition_data_src a join food_desc_src b where a.nutrient_database_number=b.nutrient_database_number ) data group by data.nutrient_database_number,data.long_description,data.short_description,data.food_group_description,data.food_group_code,data.common_name,data.manufacturer_name,data.survey,data.refused_or_inedible_part_descrption,data.percentage_ofrefuse_by_weight,data.scientific_name,data.nitrogen_to_protein_converting_factor,data.protein_factor,data.fat_factor,data.carbohydrate_factor;






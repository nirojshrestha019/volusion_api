import requests
import xml.etree.ElementTree as ET
from core.helper.XmlProcess import XmlProcess
import os
from core.config.paths import output_path
from core.config import static
from core.helper.FileCombiner import FilesCombiner


class APICaller:
    count = 1

    def __init__(self):
        self.username = static.username
        self.encrypted_password = static.encrypted_password
        self.link = "{}{}".format(
            static.link.rstrip("/").replace("https://", "").replace("http://", ""),
            "/net/WebService.aspx",
        )
        self.user_agent = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "snap Chromium/74.0.3729.169 Chrome/74.0.3729.169 Safari/537.36"
        }
        # self.flag = True
        self.API_TaxableProduct_values = ["Y", "N", "NULL"]

    def volusionapi(self, each_attribute_value):
        name = r"Generic\Products"
        columns = r"*"
        where_column = r"pe.TaxableProduct"
        val = each_attribute_value
        # columns = r'*,*,p.IsChildOfProductCode,p.IsChildOfProductCode_ProductID,p.HideProduct,p.ProductCode,' \
        #           r'p.ProductID,p.ProductName,p.Share_StockStatus_With,p.Share_StockStatus_With_ProductID,' \
        #           r'p.StockStatus,pd.ProductDescription,pd.ProductDescriptionShort,pe.Availability,pe.Book_ISBN,' \
        #           r'pe.custom_label_0,pe.custom_label_1,pe.custom_label_2,pe.custom_label_3,pe.custom_label_4,' \
        #           r'pe.Google_Adult_Product,pe.Google_Age_Group,pe.Google_Availability,pe.Google_Color,' \
        #           r'pe.Google_Gender,pe.Google_Material,pe.Google_Pattern,pe.Google_Product_Category,' \
        #           r'pe.Google_Product_Type,pe.Google_Size,pe.Google_SizeSystem,pe.Google_SizeType,pe.ProductCategory,' \
        #           r'pe.ProductCondition,pe.ProductPrice,pe.SalePrice,pe.UPC_code'
        data = {
            "Login": self.username,
            "EncryptedPassword": self.encrypted_password,
            "EDI_Name": name,
            "SELECT_Columns": columns,
            "WHERE_Column": where_column,
            "WHERE_Value": val,
        }
        try:
            r = requests.post(
                "{}{}".format("http://", self.link),
                params=data,
                headers=self.user_agent,
            )
            data = r.content.decode("utf-8")
        except requests.exceptions.ConnectionError as e:
            print("Request failed. Invalid Credentials.!!")
            exit()
        with open(
            os.path.join(output_path, "output_xml_{}.xml".format(APICaller.count)),
            "w",
            encoding="utf-8",
        ) as xmlfile:
            xmlfile.write(data)
        APICaller.count += 1
        return data

    def start(self):
        # while self.flag:
        #     data = self.volusionapi()
        #     root = ET.fromstring(data)
        #     if root.find('{}{}'.format('.//', 'Products')):
        #         print('Found')
        #         XmlProcess(root).start()
        #     else:
        #         self.flag = False
        #         print('Element not Found')
        # FilesCombiner().start()
        # print('The End')

        for each_attribute_value in self.API_TaxableProduct_values:
            data = self.volusionapi(each_attribute_value)
            root = ET.fromstring(data)
            if root.find("{}{}".format(".//", "Products")):
                print(
                    "Element found for {} values of Taxable product attribute".format(
                        each_attribute_value
                    )
                )
                XmlProcess(root).start()
                print(
                    "_______________________________________________________________________________________________"
                )
            else:
                # self.flag = False
                print(
                    "Element not Found for {} value of Taxable product attribute.".format(
                        each_attribute_value
                    )
                )
                print(
                    "_______________________________________________________________________________________________"
                )
        FilesCombiner().start()
        print("The End")

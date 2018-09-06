using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System;
using UnityEngine.UI;


public class Controller : MonoBehaviour
{
    int i = 0;
    int t = 0;
    int l = 0;
    string dtex ="";
    int d = 1;
    public float speed;
    public float theta;

    string result;

    string[] b;
    string last;

    string[] c;
    float[] ymin = new float[5];
    float[] xmin = new float[5];
    float[] ymax = new float[5];
    float[] xmax = new float[5];

    public int xwid;
    public int ywid;

    float[] rx = new float[5];
    float[] ry = new float[5];

    float[] rcol1 = new float[5];
    float[] rcol2 = new float[5];
    float[] rcol3 = new float[5];


    public Text Risk1;
    public Text Risk2;
    public Text Risk3;
    public Text Risk4;
    public Text Risk5;
    public string[] newRisk = new string[5];
    double[] newRiskf = new double[5];
    double[] newRiskff = new double[5];



    public RenderTexture screenshot;
    public RenderTexture screenshot2;


    // Use this for initialization
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

        transform.position -= transform.right * speed * 0.01f * Time.deltaTime;

        
        //ドライバー視点　テキスト表示あり
        if (i % 10 == 0)
        {
            //ドライバー視点
            ScreenCapture.CaptureScreenshot("images1/screenshot" + t + ".png");

            //俯瞰視点
            Texture2D texture2 = new Texture2D(screenshot2.width, screenshot2.height, TextureFormat.RGB24, false);
            RenderTexture.active = screenshot2;
            texture2.ReadPixels(new Rect(0, 0, screenshot2.width, screenshot2.height), 0, 0);
            texture2.Apply();
            //to PNG
            byte[] bytes2 = texture2.EncodeToPNG();
            UnityEngine.Object.Destroy(texture2);
            File.WriteAllBytes(Application.dataPath + "/images2/screenshot" + t + ".png", bytes2);
             t = t + 1;
        }


        if (i % 100 == 0)
        {
            Console.WriteLine("www");
            //transform.position -= transform.right * speed * Time.deltaTime;
            savePNG();

            if (d == 0)
            {
                transform.Rotate(new Vector3(0f, -theta, 0f));
            }
            else if (d == 2)
            {
                transform.Rotate(new Vector3(0f, theta, 0f));
            }

            //transform.Rotate(new Vector3(0f,0.01f,0f));
            //transform.Rotate(new Vector3(0f, -0.01f, 0f));

            /*
            Risk1.text =newRisk[0];
            Risk1.transform.position = new Vector3(rx[0],ry[0]);
            Risk1.color = new Color(rcol1[0]/255f,rcol2[0]/ 255f,rcol3[0]/ 255f);

            Risk2.text = newRisk[1];
            Risk2.transform.position = new Vector3(rx[1], ry[1]);
            Risk2.color = new Color(rcol1[1] / 255f, rcol2[1] / 255f, rcol3[1] / 255f);

            Risk3.text = newRisk[2];
            Risk3.transform.position = new Vector3(rx[2], ry[2]);
            Risk3.color = new Color(rcol1[2] / 255f, rcol2[2] / 255f, rcol3[2] / 255f);

            Risk4.text = newRisk[3];
            Risk4.transform.position = new Vector3(rx[3], ry[3]);
            Risk4.color = new Color(rcol1[3] / 255f, rcol2[3] / 255f, rcol3[3] / 255f);

            Risk5.text = newRisk[4];
            Risk5.transform.position = new Vector3(rx[4], ry[4]);
            Risk5.color = new Color(rcol1[4] / 255f, rcol2[4] / 255f, rcol3[4] / 255f);
            */
        }
        i += 1;
    }


    void savePNG()
    {

        //python送信用(テキスト表示なし)
        Texture2D texture = new Texture2D(screenshot.width, screenshot.height, TextureFormat.RGB24,false );
        RenderTexture.active = screenshot;
        texture.ReadPixels(new Rect(0, 0, screenshot.width, screenshot.height), 0, 0);
        texture.Apply();

        //to PNG
        byte[] bytes = texture.EncodeToPNG();
        UnityEngine.Object.Destroy(texture);


        WWWForm form = new WWWForm();
        form.AddBinaryData("post_data", bytes, "test.png","image/png");
        WWW www = new WWW("http://localhost:5000/test_api", form);
        StartCoroutine("WaitForRequest",www);

    }

    private IEnumerator WaitForRequest(WWW www)
    {
        yield return www;
        b = www.text.Split('@');
        Debug.Log(b);
        dtex = b[(b.Length) - 1];
        d = int.Parse(dtex);
        if (b.Length>=2)
        {
            if(b.Length>=6)
            {
                for (int x = 0; x <= 4; x++)
                {
                    c = b[x].Split(':');
                    ymin[x] = float.Parse(c[0]);
                    xmin[x] = float.Parse(c[1]);
                    ymax[x] = float.Parse(c[2]);
                    xmax[x] = float.Parse(c[3]);
                    rx[x] = (xwid * xmin[x] + xwid * xmax[x]) * 0.5f;
                    ry[x] = ((1.0f - ymin[x]) * ywid + (1.0f - ymax[x]) * ywid) * 0.5f;
                    newRiskf[x] = double.Parse(c[5]);
                    newRiskff[x] = Math.Round(newRiskf[x], 2, MidpointRounding.AwayFromZero);
                    newRisk[x] = newRiskff[x].ToString();
                    if (c[4] == "1.0")
                    {
                        rcol1[x] = 255f;
                        rcol2[x] = 0f;
                        rcol3[x] = 0f;
                    }
                    if (c[4] == "3.0")
                    {
                        rcol1[x] = 0f;
                        rcol2[x] = 255f;
                        rcol3[x] = 0f;
                    }

                    if (c[4] == "5.0")
                    {
                        rcol1[x] = 0f;
                        rcol2[x] = 0f;
                        rcol3[x] = 255f;
                    }
                    if (c[4] == "16.0")
                    {
                        rcol1[x] = 0f;
                        rcol2[x] = 0f;
                        rcol3[x] = 255f;
                    }

                }
            }
            else
            {
                for (int x = 0; x <= b.Length - 2; x++)
                {
                    c = b[x].Split(':');
                    ymin[x] = float.Parse(c[0]);
                    xmin[x] = float.Parse(c[1]);
                    ymax[x] = float.Parse(c[2]);
                    xmax[x] = float.Parse(c[3]);
                    rx[x] = (xwid * xmin[x] + xwid * xmax[x]) * 0.5f;
                    ry[x] = ((1.0f - ymin[x]) * ywid + (1.0f - ymax[x]) * ywid) * 0.5f;
                    newRiskf[x] = double.Parse(c[5]);
                    newRiskff[x] = Math.Round(newRiskf[x], 2, MidpointRounding.AwayFromZero);
                    newRisk[x] = newRiskff[x].ToString();
                    if (c[4] == "1.0")
                    {
                        rcol1[x] = 255f;
                        rcol2[x] = 0f;
                        rcol3[x] = 0f;
                    }
                    if (c[4] == "3.0")
                    {
                        rcol1[x] = 0f;
                        rcol2[x] = 255f;
                        rcol3[x] = 0f;
                    }

                    if (c[4] == "5.0")
                    {
                        rcol1[x] = 0f;
                        rcol2[x] = 0f;
                        rcol3[x] = 255f;
                    }
                    if (c[4] == "16.0")
                    {
                        rcol1[x] = 0f;
                        rcol2[x] = 0f;
                        rcol3[x] = 255f;
                    }

                }
            }
        } 
        if (b.Length<=5)
        {
            for (int y = 5; y>=b.Length; y--)
            {
                newRisk[y-1]= "";
            }
        }
    }


}
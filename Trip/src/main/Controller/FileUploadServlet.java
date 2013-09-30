package main.Controller;

/**
 * Created with IntelliJ IDEA.
 * User: root
 * Date: 7/9/13
 * Time: 8:52 AM
 * To change this template use File | Settings | File Templates.
 */
// Import required java libraries


import org.apache.http.HttpEntity;
import org.apache.http.HttpException;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.client.HttpClient;

import org.apache.http.HttpResponse;
import org.apache.http.util.EntityUtils;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.*;
import java.net.MalformedURLException;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.Iterator;
import java.util.List;

public class FileUploadServlet extends HttpServlet {
    public static final String REQ_PARAMETER = "file";
    //    private static Logger logger = Logger.getLogger(FileUploadServlet.class);

    public static final String hostname="http://localhost:8080";
    public void doPost(HttpServletRequest request,
                       HttpServletResponse response)
            throws ServletException, IOException {
        String currDir = System.getProperty("user.dir");
        String text = request.getParameter(REQ_PARAMETER);
        System.out.println(text);
        Writer writer = null;
        String currentPath=this.getClass().getClassLoader().getResource("").getPath();
        String projPath=currentPath.split("out/")[0];
        try {
            HttpGet request1 = null;
            try {
                request1 = new HttpGet("http://localhost:8000/tagSearch/" + text);
            } catch (URISyntaxException e) {
                e.printStackTrace();  //To change body of catch statement use File | Settings | File Templates.
            }

            HttpClient httpClient = new DefaultHttpClient();
            HttpResponse response1 = httpClient.execute(request1);
            HttpEntity entity = response1.getEntity();

            String jsonData = EntityUtils.toString(entity);

            String jsonFilePath=projPath+"web/jsonData.json" ;
            try{
            writer = new BufferedWriter(new OutputStreamWriter(
                    new FileOutputStream(jsonFilePath), "utf-8"));
            writer.write(jsonData);
            }
            catch (IOException e) {
                e.printStackTrace();
            }

            finally {
                try {
                    writer.close();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (HttpException e) {
            e.printStackTrace();  //To change body of catch statement use File | Settings | File Templates.
        }


//        // Check that we have a file upload request
//        isMultipart = ServletFileUpload.isMultipartContent(request);
        response.sendRedirect(hostname+"/timeline.html");
    }

    public void doGet(HttpServletRequest request,
                      HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
//        throw new ServletException("GET method used with " +
//                getClass( ).getName( )+": POST method required.");
    }
}

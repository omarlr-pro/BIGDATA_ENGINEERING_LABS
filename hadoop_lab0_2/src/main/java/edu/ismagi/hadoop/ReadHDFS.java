package edu.ismagi.hadoop;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.*;

public class ReadHDFS {
    public static void main(String[] args) throws IOException {
        if (args.length < 1) {
            System.err.println("Usage: ReadHDFS <hdfs_path>");
            System.exit(1);
        }
        String hdfsPath = args[0]; // ex: /user/root/input/purchases.txt
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);

        Path path = new Path(hdfsPath);
        if (!fs.exists(path)) {
            System.err.println("File does not exist: " + hdfsPath);
            System.exit(1);
        }
        try (FSDataInputStream inStream = fs.open(path);
             BufferedReader br = new BufferedReader(new InputStreamReader(inStream))) {
            String line;
            while ((line = br.readLine()) != null) {
                System.out.println(line);
            }
        } finally {
            fs.close();
        }
    }
}
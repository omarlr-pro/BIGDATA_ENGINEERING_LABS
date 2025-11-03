package edu.ismagi.hadoop;

import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.*;

public class HDFSWrite {
    public static void main(String[] args) throws IOException {
        if (args.length < 1) {
            System.err.println("Usage: HDFSWrite <hdfs_path> [text_to_write]");
            System.exit(1);
        }
        String hdfsPath = args[0]; // ex: /input/bonjour.txt
        String text = (args.length >= 2) ? args[1] : "Bonjour tout le monde !";

        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        Path path = new Path(hdfsPath);

        if (!fs.exists(path)) {
            try (FSDataOutputStream out = fs.create(path)) {
                out.writeUTF(text);
                // Optionally write more lines: out.writeBytes("\nAutre ligne\n");
            }
            System.out.println("Wrote to " + hdfsPath);
        } else {
            System.err.println("File already exists: " + hdfsPath);
        }
        fs.close();
    }
}
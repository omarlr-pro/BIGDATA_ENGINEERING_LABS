package edu.ismagi.hadoop;

import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.*;

public class HadoopFileStatus {
    public static void main(String[] args) {
        if (args.length < 3) {
            System.err.println("Usage: HadoopFileStatus <hdfs_dir> <filename> <newfilename>");
            System.exit(1);
        }
        String dir = args[0];            // ex: /user/root/input
        String filename = args[1];       // ex: purchases.txt
        String newname = args[2];        // ex: achats.txt

        Configuration conf = new Configuration();
        try {
            FileSystem fs = FileSystem.get(conf);
            Path filepath = new Path(dir, filename);
            if (!fs.exists(filepath)) {
                System.out.println("File does not exist: " + filepath);
                System.exit(1);
            }
            FileStatus status = fs.getFileStatus(filepath);
            System.out.println("File Name: " + filepath.getName());
            System.out.println("File Size: " + status.getLen() + " bytes");
            System.out.println("File owner: " + status.getOwner());
            System.out.println("File permission: " + status.getPermission());
            System.out.println("File Replication: " + status.getReplication());
            System.out.println("File Block Size: " + status.getBlockSize());

            BlockLocation[] blockLocations = fs.getFileBlockLocations(status, 0, status.getLen());
            for (BlockLocation blockLocation : blockLocations) {
                String[] hosts = blockLocation.getHosts();
                System.out.println("Block offset: " + blockLocation.getOffset());
                System.out.println("Block length: " + blockLocation.getLength());
                System.out.print("Block hosts: ");
                for (String host : hosts) {
                    System.out.print(host + " ");
                }
                System.out.println();
            }

            // rename file
            Path newpath = new Path(dir, newname);
            boolean renamed = fs.rename(filepath, newpath);
            System.out.println("Rename " + (renamed ? "succeeded" : "failed") + " -> " + newpath);

            fs.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
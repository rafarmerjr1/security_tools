import boto3
import csv

# Amazon S3 and variable declarations
s3 = boto3.resource('s3')
client = boto3.client('s3')
client_rds = boto3.client('rds')
client_redshift = boto3.client('redshift')
client_efs = boto3.client('efs')

# Create some empty lists
bucket_list = []
rds_list = []
encrypted_snapshot_list = []
unencrypted_snapshot_list = []
snapshot_list = []
redshift_list =[]
efs_list = []

global total_encrypted_buckets
global total_unencrypted_buckets
encrypted_s3_buckets = []
unencrypted_s3_buckets = []

#Program starts here
###################################################################################
def get_list():
    for bucket in s3.buckets.all():
        bucket_list.append(bucket.name)

def get_s3_encryption():
    i = 0
    j = 0
    with open('Encrypted_s3.csv', 'w', newline = '') as f:
        write = csv.writer(f)
        write.writerow(["Encrypted buckets"])
        for item in bucket_list:
            try:
                response2 = client.get_bucket_encryption(Bucket=item)['ServerSideEncryptionConfiguration']
                response = response2["Rules"]
                for s in range(len(response)):
                    print("{} : {}".format(item, response[s]['ApplyServerSideEncryptionByDefault']))
                    write.writerow([item, response[s]['ApplyServerSideEncryptionByDefault']])
                    i += 1
            except:
                j += 1
                print("%s *****No Encryption Found*****" % item)
                unencrypted_s3_buckets.append(item)
    total_encrypted_buckets = i
    total_unencrypted_buckets = j
    print("Total Encrypted buckets %i" % total_encrypted_buckets)
    print("Total Unencrypted buckets %i" % total_unencrypted_buckets)
    print("Writing to Encrypted_s3.csv and Unencrypted_s3.csv...")

#Placed in its own function since we're writing to two files (encrypted and unencrypted)
def write_s3_results():
    with open('Unencrypted_s3.csv', 'w', newline = '') as f2:
        write =csv.writer(f2)
        write.writerow(["Unencrypted Buckets"])
        for bn in unencrypted_s3_buckets:
            write.writerow([bn])
        f2.close()

def get_rds_list():
    db_instances = client_rds.describe_db_instances()
    for i in range(len(db_instances['DBInstances'])):
        DBName = db_instances['DBInstances'][i]['DBInstanceIdentifier']
        rds_list.append(DBName)
    print(len(db_instances['DBInstances']))

def get_rds_encryption():
    with open('RDS.csv', 'w', newline = '') as f3:
        write = csv.writer(f3)
        for rds_item in rds_list:
            rds_response = client_rds.describe_db_instances(DBInstanceIdentifier=rds_item)["DBInstances"]
            for s in range(len(rds_response)):
                print("{} : {}".format(rds_response[s]["DBInstanceIdentifier"], rds_response[s]["StorageEncrypted"]))
                RDS_name = rds_response[s]["DBInstanceIdentifier"]
                RDS_crypt = rds_response[s]["StorageEncrypted"]
                write.writerow([RDS_name, RDS_crypt])
        f3.close()

def get_redshift():
    clusters = client_redshift.describe_clusters()
    for i in range(len(clusters["Clusters"])):
        RedShift_Name = clusters["Clusters"][i]['ClusterIdentifier']
        redshift_list.append(RedShift_Name)

def get_redshift_encryption():
    with open('Redshift.csv', 'w', newline = '') as f4:
        write = csv.writer(f4)
        for redshift_item in redshift_list:
            redshift_response = client_redshift.describe_clusters(ClusterIdentifier=redshift_item)["Clusters"]
            for s in range(len(redshift_response)):
                print("{} : {}".format(redshift_response[s]["ClusterIdentifier"],redshift_response[s]["Encrypted"]))
                rs_name = redshift_response[s]["ClusterIdentifier"]
                rs_crypt = redshift_response[s]["Encrypted"]
                write.writerow([rs_name, rs_crypt])
        f4.close()

def get_EFS():
    response = client_efs.describe_file_systems()
    for i in range(len(response['FileSystems'])):
        efs_id = response['FileSystems'][i]['FileSystemId']
        efs_list.append(efs_id)

def get_efs_encryption():
    with open('EFS.csv', 'w', newline = '') as f5:
        write = csv.writer(f5)
        for efs_item in efs_list:
            efs_response = client_efs.describe_file_systems(FileSystemId=efs_item)['FileSystems']
            for s in range(len(efs_response)):
                print("{} : {}".format(efs_response[s]['Name'],efs_response[s]["Encrypted"]))
                efs_name = efs_response[s]['Name']
                efs_crypt = efs_response[s]["Encrypted"]
                write.writerow([efs_name, efs_crypt])
        f5.close()

def get_RDS_snapshots2(): #Does AWS constrain this to 100 requests? Paginate.
        paginator = client_rds.get_paginator('describe_db_snapshots')
        response = paginator.paginate()
        count = 0
        for i in response:
             u = i['DBSnapshots']
             for snap in u:
                 snap_name = snap['DBSnapshotIdentifier']
                 snap_crypt = snap['Encrypted']
                 snap_stats = snap_name + str(snap_crypt)
                 if snap['Encrypted'] == False:
                    print(snap_name,snap_crypt)
                    unencrypted_snapshot_list.append(snap_stats)
                 elif snap['Encrypted'] == True:
                    encrypted_snapshot_list.append(snap_stats)
                 count += 1
                 #print("{} : {}".format(snap_name,snap_crypt))
        print(count)
        print(len(encrypted_snapshot_list))
        print(len(unencrypted_snapshot_list))

def get_snapshot_encryption_csvs():
        with open('snapshots.csv', 'w', newline = '') as f6:
            write = csv.writer(f6)
            for snapshot in snapshot_list:
                snapshot_response = client_rds.describe_db_snapshots(DBSnapshotIdentifier=snapshot)['DBSnapshots']
                for s in range(len(snapshot_response)):
                    print("{} : {}".format(snapshot_response[s]['DBSnapshotIdentifier'],snapshot_response[s]['Encrypted']))
                    snap_name = snapshot_response[s]['DBSnapshotIdentifier']
                    snap_crypt = snapshot_response[s]['Encrypted']
                    write.writerow([snap_name, snap_crypt])


def complete_scan():
    get_list()
    get_s3_encryption()
    write_s3_results()
    get_rds_list()
    get_rds_encryption()
    get_redshift()
    get_redshift_encryption()
    get_EFS()
    get_efs_encryption()
    print("\n\nCheck for output files:: Encrypted_s3.csv, Unencrypted_s3.csv, EFS.csv, RDS.csv, and Redshift.csv.\n\n")

#get_list()
#get_s3_encryption()
#write_s3_results()
#get_rds_list()
#get_rds_encryption()
#get_redshift()
#get_redshift_encryption()
#get_EFS()
#get_efs_encryption()
#get_RDS_snapshots2()
#get_snapshot_encryption_csvs()
complete_scan()

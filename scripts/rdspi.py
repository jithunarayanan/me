import time
import boto3
import datetime

pi_client = boto3.client('pi')
rds_client = boto3.client('rds')
cw_client = boto3.client('cloudwatch')

CUSTOM_NAMESPACE = 'RDSPerformanceInsights'

engine_metrics = {
    'aurora': ['db.SQL.Innodb_rows_read.avg'],
    'aurora-postgresql': ['db.Transactions.xact_commit.avg'],
    'postgres': ['db.Transactions.xact_commit.avg'],
    'mysql': [   # Adding MySQL example metrics here
        # 'db.load.avg',
        # 'os.cpuUtilization.user.avg',
        # 'os.cpuUtilization.system.avg',
        # 'os.cpuUtilization.nice.avg',
        # 'os.cpuUtilization.steal.avg',
        # 'os.cpuUtilization.guest.avg',
        # 'os.cpuUtilization.irq.avg',
        # 'os.cpuUtilization.wait.avg',
        # 'os.diskIO.nvme1n1.readIOsPS.avg',
        # 'os.diskIO.nvme1n1.writeIOsPS.avg',
        # 'db.Users.Aborted_clients.avg',
        # 'db.Users.Threads_running.avg',
        # 'os.network.tx.avg', 
        # 'os.network.rx.avg',
        # 'db.Cache.Innodb_buffer_pool_reads.avg',
        'db.Cache.innoDB_buffer_pool_hit_rate.avg',
        'db.Cache.innoDB_buffer_pool_hits.avg',
        'db.Transactions.active_transactions.avg',
        'db.Locks.innodb_row_lock_waits.avg',
        'db.SQL.Com_select.avg',
        'db.SQL.Innodb_rows_deleted.avg',
        'db.SQL.Innodb_rows_updated.avg',
        'db.SQL.Innodb_rows_inserted.avg',
        'db.SQL.Queries.avg',
        'db.Locks.innodb_deadlocks.avg',
        'db.Locks.Innodb_row_lock_time.avg',
        'db.Users.Connections.avg',
        'db.Users.Threads_connected.avg',
        'db.Transactions.trx_rseg_history_len.avg'
    ]
}

def lambda_handler(event, context):
    pi_instances = get_pi_instances()

    for instance in pi_instances:
        pi_response = get_resource_metrics(instance)
        if pi_response:
            send_cloudwatch_data(pi_response)

    return {
        'statusCode': 200,
        'body': 'Successfully pushed RDS Performance Insights metrics to custom CloudWatch namespace.'
    }


def get_pi_instances():
    response = rds_client.describe_db_instances()
    return filter(
        lambda _: _.get('PerformanceInsightsEnabled', False),   
        response['DBInstances']
    )


def get_resource_metrics(instance):
    metric_queries = []
    if engine_metrics.get(instance['Engine'], False):
        for metric in engine_metrics[instance['Engine']]:
            metric_queries.append({'Metric': metric})

    if not metric_queries:
        return

    now = datetime.datetime.utcnow()
    start_time = now - datetime.timedelta(minutes=5)

    return pi_client.get_resource_metrics(
        ServiceType='RDS',
        Identifier=instance['DbiResourceId'],
        StartTime=start_time,
        EndTime=now,
        PeriodInSeconds=60,
        MetricQueries=metric_queries
    )


def send_cloudwatch_data(pi_response):
    metric_data = []

    for metric_response in pi_response['MetricList']:
        cur_key = metric_response['Key']['Metric']

        for datapoint in metric_response['DataPoints']:
            value = datapoint.get('Value', None)

            if value is not None:
                metric_data.append({
                    'MetricName': cur_key,
                    'Dimensions': [
                        {
                            'Name': 'jithu',
                            'Value': pi_response['Identifier']
                        }
                    ],
                    'Timestamp': datapoint['Timestamp'],
                    'Value': value
                })

    if metric_data:
        cw_client.put_metric_data(
            Namespace=CUSTOM_NAMESPACE,
            MetricData=metric_data
        )

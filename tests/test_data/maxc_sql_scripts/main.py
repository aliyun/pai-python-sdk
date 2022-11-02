import argparse
import json

from pai_running.context import Context
from pai_running.executor import MaxComputeExecutor, MaxComputeSqlUtils, SqlJob


def prepare():
    parser = argparse.ArgumentParser("Tensorflow template arguments parser")
    parser.add_argument("--sql")
    parser.add_argument("--execution")
    parser.add_argument("--lifeCycle")
    parser.add_argument("--outputTable")
    args, _ = parser.parse_known_args()
    context = Context()
    return args, context


def build_sql(sql, context):
    print("build_sql: input raw SQL is %s" % sql)
    for idx, artifact in enumerate(context.input_artifacts):
        if not artifact.raw_value:
            continue
        placeholder = "${%s}" % artifact.name
        table = artifact.get_table()
        sql = sql.replace(placeholder, table)
    sql_sentences = MaxComputeSqlUtils.split(sql)
    if len(sql_sentences) == 0:
        raise ValueError("expect no empty SQL.")
    last_sql = sql_sentences.pop(-1)
    if not last_sql.strip().lower().startswith("select"):
        raise ValueError("require SELECT sentence to be used as the last SQL.")
    dest_table = context.input_parameters["outputTable"]

    last_sql = " ".join(["create table ", dest_table, "as", last_sql])

    sql_sentences.append(last_sql)
    return "\n".join(sql_sentences), dest_table


def main():
    args, run_context = prepare()
    maxc_execution = json.loads(args.execution)
    max_compute_executor = MaxComputeExecutor.from_config(maxc_execution)

    sql_script, dest_table = build_sql(args.sql, run_context)

    print("Proceeded SQL script:%s" % sql_script)

    job = SqlJob(
        sql=sql_script,
        delete_tables=dest_table,
    )
    max_compute_executor.submit(job)


if __name__ == "__main__":
    main()

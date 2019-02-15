import argparse
import code
from fs import osfs
from .context import Context, RUN_MODES
from . import read_config, get_logger, create_engine, constants
from . import provinces, departments, municipalities, localities, streets
from . import countries, intersections

DATA_PATH = 'data'
PROCESSES = [
    constants.PROVINCES,
    constants.DEPARTMENTS,
    constants.MUNICIPALITIES,
    constants.LOCALITIES,
    constants.STREETS,
    constants.INTERSECTIONS
]


def parse_args():
    parser = argparse.ArgumentParser(
        prog='georef_ar_etl',
        description='ETL para Georef. Versión: {}.'.format(
            constants.ETL_VERSION)
    )
    parser.add_argument('-p', '--processes', action='append',
                        choices=PROCESSES, help='Procesos ETL a ejecutar.')
    parser.add_argument('-m', '--mode', choices=RUN_MODES, default='normal',
                        help='Modo de ejecución.')
    parser.add_argument('-c', '--console', action='store_true',
                        help='Iniciar una consola interactiva.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Imprimir información adicional.')

    return parser.parse_args()


def etl(enabled_processes, ctx):
    processes = [
        countries.CountriesETL(),
        provinces.ProvincesETL(),
        departments.DepartmentsETL(),
        municipalities.MunicipalitiesETL(),
        localities.LocalitiesETL(),
        streets.StreetsETL(),
        intersections.IntersectionsETL()
    ]

    for process in processes:
        if not enabled_processes or process.name in enabled_processes:
            process.run(ctx)


def console(ctx):
    console = code.InteractiveConsole(locals=locals())
    console.push('from georef_ar_etl import models')
    console.interact()


def main():
    args = parse_args()
    config = read_config()

    ctx = Context(
        config=config,
        data_fs=osfs.OSFS(DATA_PATH),
        cache_fs=osfs.OSFS(config.get('etl', 'cache_dir'), create=True,
                           create_mode=0o700),
        engine=create_engine(config, echo=args.verbose),
        logger=get_logger(),
        mode=args.mode
    )

    if args.console:
        console(ctx)
    else:
        etl(args.processes, ctx)


main()

import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import TableBody from '@material-ui/core/TableBody';

import DisplaysTableItem from './DisplaysTableItem.jsx';

const styles = theme => ({
    table: {
        borderSpacing: '0',
        borderCollapse: 'collapse',
    },
    tableTitles: {
        '@media (max-width: 1200px)': {
            display: 'none',
        },
    },
    tableResponsive: {
        overflowX: 'auto',
    },
});

function DisplaysTable({
    onDeleteDisplay,
    classes,
    items,
    onEditDevice,
    onEditDisplay,
    deviceList,
}) {
    return (
        <div className={classes.tableResponsive}>
            <Table className={classes.table}>
                <TableHead>
                    <TableRow className={classes.tableTitles}>
                        <TableCell></TableCell>
                        <TableCell>Name</TableCell>
                        <TableCell>Max Brightness</TableCell>
                        <TableCell>Crossfade</TableCell>
                        <TableCell>Center-Offset</TableCell>
                        <TableCell>Preview-Only</TableCell>
                        <TableCell />
                    </TableRow>
                </TableHead>

                <TableBody>
                    {items.map(display => (
                        <DisplaysTableItem
                            key={display.id}
                            display={display}
                            deviceList={deviceList}
                            onDelete={onDeleteDisplay}
                            onEditDevice={onEditDevice}
                            onEditDisplay={onEditDisplay}
                        />
                    ))}
                </TableBody>
            </Table>
        </div>
    );
}

DisplaysTable.propTypes = {
    classes: PropTypes.object.isRequired,
    items: PropTypes.array.isRequired,
};

export default withStyles(styles)(DisplaysTable);
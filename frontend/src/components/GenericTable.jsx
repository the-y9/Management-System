import { Table } from "react-bootstrap";

export default function GenericTable({ colHeaders, data, renderActions, variant, rowKey, highlightColumnKey }) {
    
    return (<>
        <Table striped bordered hover variant={variant} size='sm'>
            <thead>
                <tr>
                    {colHeaders.map((col) => (
                         <th key={col.key}
                            className={col.key === highlightColumnKey ? "highlight-col" : ""}
                        >{col.label}</th>
                    ))}
                    {renderActions && (<th>Actions</th>)}
                </tr>
            </thead>
            <tbody>
                {data.map((item) => (
                    <tr key={item[rowKey]}>
                        {colHeaders.map((col) => (
                            <td key={col.key}
                                className={col.key === highlightColumnKey ? "highlight-col" : ""}
                            >{item[col.key]}</td>
                        ))}
                        {renderActions && (
                            <td className="d-flex gap-2">
                                {renderActions(item)}
                            </td>
                        )}
                    </tr>
                ))}
            </tbody>
        </Table>
        </>);
}